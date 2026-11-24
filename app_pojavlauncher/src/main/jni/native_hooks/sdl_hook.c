
#include "environ/environ.h"
#include "utils.h"
#include "native_hooks.h"
#include "log.h"
#include "SDL3/SDL.h"

#include <bytehook.h>
#include <dlfcn.h>
#include <jni.h>
#include <stdlib.h>
#include <string.h>
#include <pthread.h>

#include "../ctxbridges/loader_dlopen.h"

DECL_DLSYM(SDL_InitSubSystem)
DECL_DLSYM(SDL_OpenGamepad)
DECL_DLSYM(SDL_OpenJoystick)
DECL_DLSYM(SDL_CloseGamepad)
DECL_DLSYM(SDL_CloseJoystick)
DECL_DLSYM(SDL_SetHint);
DECL_DLSYM(SDL_SetTextInputArea);
DECL_DLSYM(SDL_SetError);
DECL_DLSYM(SDL_GetError);
DECL_DLSYM(SDL_LoadObject)
DECL_DLSYM(SDL_CreateWindow)
DECL_DLSYM(SDL_DestroyWindow)


static bool custom_SDL_InitSubSystem_Func(SDL_InitFlags flags) {
    // Call notifyLauncher on SDL_InitSubSystem, this sets up all the JNI stuff needed by SDL.
    TRY_ATTACH_ENV(dvm_env, pojav_environ->dalvikJavaVMPtr, "SDL_InitSubSystem failed!",
            SET_DLSYM_PTR(dlopen("libSDL3.so", RTLD_NOLOAD), SDL_SetError);
            if (SDL_SetError_p) SDL_SetError_p("Failed to load SDL launcher integration android-side. This is not an SDL bug, please contact the launcher developer.");
            return false;
            );

    // Just in case of bozo
    jint safeFlags;
    if (flags > INT32_MAX) {
        safeFlags = -1;
    } else safeFlags = (jint)flags;

    notifyLauncher(dvm_env, NOTIF_TYPE_SDL, (int[]){ACTION_INIT_LAUNCHER_INTEGRATION, safeFlags}, 2);

    // This is the normal for the launcher, the default in SDL is false.
    SET_DLSYM_PTR(dlopen("libSDL3.so", RTLD_NOLOAD), SDL_SetHint);
    if (SDL_SetHint_p) SDL_SetHint_p("SDL_RETURN_KEY_HIDES_IME", "true");
    // FIXME: MobileGlues has issues with passing in the proper EGL params to make this work
    const char *egl = getenv("POJAVEXEC_EGL");
    if (egl && strcmp(egl, "libmobileglues.so") == 0) {
        SDL_SetHint_p("SDL_OPENGL_FORCE_SRGB_FRAMEBUFFER", "0");
    }

    // Call original func after doing all the needed setup
    bool r = BYTEHOOK_CALL_PREV(custom_SDL_InitSubSystem_Func, SDL_InitSubSystem_t, flags);
    if (!r){
        SET_DLSYM_PTR(dlopen("libSDL3.so", RTLD_NOLOAD), SDL_GetError);
        LOGI("Amethyst-Android: SDL_InitSubsystem Error: %s", SDL_GetError_p());
    }
    BYTEHOOK_POP_STACK();
    return r;
}

//// This doesn't work because lwjgl doesn't use plt/got to access the bindings, fml
//static bool custom_SDL_SetTextInputArea_Func(SDL_Window *window, const SDL_Rect *rect, int cursor) {
//    TRY_ATTACH_ENV(SDL_GetTextInputArea);
//    notifyLauncher(dvm_env, NOTIF_TYPE_SDL, (int[]) {
//        ACTION_SEND_TEXTBOX_RECT,
//        rect->x, rect->y, rect->x + rect->w, rect->y + rect->h, cursor
//    }, 6);
//    int r = BYTEHOOK_CALL_PREV(custom_SDL_SetTextInputArea_Func, SDL_SetTextInputArea_t, window, rect, cursor);
//    BYTEHOOK_POP_STACK();
//    return r;
//}

/*
 * Tracked handle lists
 */
typedef struct joystick_node {
    SDL_Joystick *handle;
    struct joystick_node *next;
} joystick_node_t;

typedef struct gamepad_node {
    SDL_Gamepad *handle;
    struct gamepad_node *next;
} gamepad_node_t;

static pthread_mutex_t g_sdl_handles_mutex =
        PTHREAD_MUTEX_INITIALIZER;

static joystick_node_t *g_joysticks = NULL;
static gamepad_node_t *g_gamepads = NULL;

static int g_joystick_count = 0;
static int g_gamepad_count = 0;
static int g_active_sdl_device_count = 0;

/*
 * Called when the first SDL joystick/gamepad becomes active.
 */
static void on_sdl_input_active(void)
{
    LOGI("SDL controller integration active");
    TRY_ATTACH_ENV(dvm_env, pojav_environ->dalvikJavaVMPtr, "SDL_InitSubSystem failed!",
            SET_DLSYM_PTR(dlopen("libSDL3.so", RTLD_NOLOAD), SDL_SetError);
            if (SDL_SetError_p) SDL_SetError_p("Failed to load SDL launcher integration android-side. This is not an SDL bug, please contact the launcher developer.");
            return;
    );
    notifyLauncher(dvm_env, NOTIF_TYPE_SDL, (int[]){ACTION_INIT_CONTROLLER}, 1);

}

/*
 * Called when the last SDL joystick/gamepad becomes inactive.
 */
static void on_sdl_input_inactive(void)
{
    LOGI("SDL controller integration inactive");
    TRY_ATTACH_ENV(dvm_env, pojav_environ->dalvikJavaVMPtr, "SDL_InitSubSystem failed!",
            SET_DLSYM_PTR(dlopen("libSDL3.so", RTLD_NOLOAD), SDL_SetError);
            if (SDL_SetError_p) SDL_SetError_p("Failed to load SDL launcher integration android-side. This is not an SDL bug, please contact the launcher developer.");
            return;
    );
    notifyLauncher(dvm_env, NOTIF_TYPE_SDL, (int[]){ACTION_DEINIT_CONTROLLER}, 1);
}

/*
 * Joystick tracking
 */
static void track_joystick(SDL_Joystick *joystick)
{
    joystick_node_t *node;
    int became_active = 0;

    if (joystick == NULL)
        return;

    node = malloc(sizeof(*node));
    if (node == NULL) {
        LOGI("Failed to allocate joystick tracking node");
        return;
    }

    node->handle = joystick;

    pthread_mutex_lock(&g_sdl_handles_mutex);

    node->next = g_joysticks;
    g_joysticks = node;

    g_joystick_count++;

    if (g_active_sdl_device_count == 0)
        became_active = 1;

    g_active_sdl_device_count++;

    pthread_mutex_unlock(&g_sdl_handles_mutex);

    if (became_active)
        on_sdl_input_active();
}

static void untrack_joystick(SDL_Joystick *joystick)
{
    joystick_node_t **current;
    int became_inactive = 0;

    if (joystick == NULL)
        return;

    pthread_mutex_lock(&g_sdl_handles_mutex);

    current = &g_joysticks;

    while (*current != NULL) {
        if ((*current)->handle == joystick) {
            joystick_node_t *removed = *current;

            *current = removed->next;
            free(removed);

            if (g_joystick_count > 0)
                g_joystick_count--;

            if (g_active_sdl_device_count > 0)
                g_active_sdl_device_count--;

            if (g_active_sdl_device_count == 0)
                became_inactive = 1;

            break;
        }

        current = &(*current)->next;
    }

    pthread_mutex_unlock(&g_sdl_handles_mutex);

    if (became_inactive)
        on_sdl_input_inactive();
}

/*
 * Gamepad tracking
 */
static void track_gamepad(SDL_Gamepad *gamepad)
{
    gamepad_node_t *node;
    int became_active = 0;

    if (gamepad == NULL)
        return;

    node = malloc(sizeof(*node));
    if (node == NULL) {
        LOGI("Failed to allocate gamepad tracking node");
        return;
    }

    node->handle = gamepad;

    pthread_mutex_lock(&g_sdl_handles_mutex);

    node->next = g_gamepads;
    g_gamepads = node;

    g_gamepad_count++;

    if (g_active_sdl_device_count == 0)
        became_active = 1;

    g_active_sdl_device_count++;

    pthread_mutex_unlock(&g_sdl_handles_mutex);

    if (became_active)
        on_sdl_input_active();
}

static void untrack_gamepad(SDL_Gamepad *gamepad)
{
    gamepad_node_t **current;
    int became_inactive = 0;

    if (gamepad == NULL)
        return;

    pthread_mutex_lock(&g_sdl_handles_mutex);

    current = &g_gamepads;

    while (*current != NULL) {
        if ((*current)->handle == gamepad) {
            gamepad_node_t *removed = *current;

            *current = removed->next;
            free(removed);

            if (g_gamepad_count > 0)
                g_gamepad_count--;

            if (g_active_sdl_device_count > 0)
                g_active_sdl_device_count--;

            if (g_active_sdl_device_count == 0)
                became_inactive = 1;

            break;
        }

        current = &(*current)->next;
    }

    pthread_mutex_unlock(&g_sdl_handles_mutex);

    if (became_inactive)
        on_sdl_input_inactive();
}

/*
 * Hook functions
 */
static SDL_Joystick *
custom_SDL_OpenJoystick_Func(SDL_JoystickID instance_id)
{
    SDL_Joystick *result;

    LOGI("SDL_OpenJoystick(%d)", (int)instance_id);

    result = BYTEHOOK_CALL_PREV(
            custom_SDL_OpenJoystick_Func,
            SDL_OpenJoystick_t,
            instance_id
    );

    BYTEHOOK_POP_STACK();

    if (result != NULL) {
        track_joystick(result);

        LOGI(
                "Joystick opened: %p, active devices: %d",
                result,
                g_active_sdl_device_count
        );
    }

    return result;
}

static SDL_Gamepad *
custom_SDL_OpenGamepad_Func(SDL_JoystickID instance_id)
{
    SDL_Gamepad *result;

    LOGI("SDL_OpenGamepad(%d)", (int)instance_id);

    result = BYTEHOOK_CALL_PREV(
            custom_SDL_OpenGamepad_Func,
            SDL_OpenGamepad_t,
            instance_id
    );

    BYTEHOOK_POP_STACK();

    if (result != NULL) {
        track_gamepad(result);

        LOGI(
                "Gamepad opened: %p, active devices: %d",
                result,
                g_active_sdl_device_count
        );
    }

    return result;
}

static void
custom_SDL_CloseJoystick_Func(SDL_Joystick *joystick)
{
    LOGI("SDL_CloseJoystick(%p)", joystick);

    BYTEHOOK_CALL_PREV(
            custom_SDL_CloseJoystick_Func,
            SDL_CloseJoystick_t,
            joystick
    );

    BYTEHOOK_POP_STACK();

    untrack_joystick(joystick);

    LOGI(
            "Joystick closed: %p, active devices: %d",
            joystick,
            g_active_sdl_device_count
    );
}

static void
custom_SDL_CloseGamepad_Func(SDL_Gamepad *gamepad)
{
    LOGI("SDL_CloseGamepad(%p)", gamepad);

    BYTEHOOK_CALL_PREV(
            custom_SDL_CloseGamepad_Func,
            SDL_CloseGamepad_t,
            gamepad
    );

    BYTEHOOK_POP_STACK();

    untrack_gamepad(gamepad);

    LOGI(
            "Gamepad closed: %p, active devices: %d",
            gamepad,
            g_active_sdl_device_count
    );
}

/*
 * The launcher's EGL (zink/Mesa) lives in the APK lib dir and SDL loads it with
 * a plain dlopen(), which some Android builds refuse (namespace restrictions or
 * RTLD_NOW on symbols the system private libs don't expose). Retry through the
 * launcher loader, which falls back to a namespace-bypass dlopen.
 */
static SDL_SharedObject *
custom_SDL_LoadObject_Func(const char *sofile)
{
    SDL_SharedObject *result = BYTEHOOK_CALL_PREV(
            custom_SDL_LoadObject_Func,
            SDL_LoadObject_t,
            sofile
    );

    BYTEHOOK_POP_STACK();

    if (result != NULL || sofile == NULL)
        return result;

    const char *renderer_egl = getenv("POJAVEXEC_EGL");
    if (renderer_egl == NULL || renderer_egl[0] == '\0')
        return NULL;

    const char *base = strrchr(sofile, '/');
    base = base ? base + 1 : sofile;
    if (strcmp(base, renderer_egl) != 0)
        return NULL;

    LOGI("SDL_LoadObject: plain dlopen of %s failed, retrying through loader_dlopen", sofile);
    void *handle = loader_dlopen((char *)sofile, (char *)base, RTLD_LOCAL | RTLD_LAZY);
    if (handle == NULL) {
        LOGI("SDL_LoadObject: loader_dlopen also failed for %s", sofile);
        return NULL;
    }
    LOGI("SDL_LoadObject: loaded %s through loader_dlopen", sofile);
    return (SDL_SharedObject *)handle;
}

/*
 * SDL's Android driver only allows one window per process. Minecraft 26.x's
 * OpenGL backend (renderpearl GlDevice) opens extra hidden helper windows, so
 * its second SDL_CreateWindow always fails there. Hand out the existing window
 * instead and keep it alive until every alias has been destroyed.
 */
static pthread_mutex_t g_sdl_window_mutex = PTHREAD_MUTEX_INITIALIZER;
static SDL_Window *g_sdl_shared_window = NULL;
static int g_sdl_shared_window_refs = 0;

static SDL_Window *
custom_SDL_CreateWindow_Func(const char *title, int w, int h, SDL_WindowFlags flags)
{
    SDL_Window *result = BYTEHOOK_CALL_PREV(
            custom_SDL_CreateWindow_Func,
            SDL_CreateWindow_t,
            title,
            w,
            h,
            flags
    );

    BYTEHOOK_POP_STACK();

    if (result != NULL) {
        pthread_mutex_lock(&g_sdl_window_mutex);
        if (g_sdl_shared_window == NULL) {
            g_sdl_shared_window = result;
            g_sdl_shared_window_refs = 1;
        }
        pthread_mutex_unlock(&g_sdl_window_mutex);
        return result;
    }

    SET_DLSYM_PTR(dlopen("libSDL3.so", RTLD_NOLOAD), SDL_GetError);
    const char *error = SDL_GetError_p ? SDL_GetError_p() : NULL;
    if (error == NULL || strstr(error, "only supports one window") == NULL)
        return NULL;

    pthread_mutex_lock(&g_sdl_window_mutex);
    if (g_sdl_shared_window == NULL) {
        pthread_mutex_unlock(&g_sdl_window_mutex);
        return NULL;
    }
    g_sdl_shared_window_refs++;
    SDL_Window *shared = g_sdl_shared_window;
    pthread_mutex_unlock(&g_sdl_window_mutex);

    LOGI("SDL_CreateWindow: Android only supports one window, reusing %p for \"%s\"",
            shared, title ? title : "");
    return shared;
}

static void
custom_SDL_DestroyWindow_Func(SDL_Window *window)
{
    int destroy = 1;

    pthread_mutex_lock(&g_sdl_window_mutex);
    if (window != NULL && window == g_sdl_shared_window) {
        if (g_sdl_shared_window_refs > 1) {
            g_sdl_shared_window_refs--;
            destroy = 0;
        } else {
            g_sdl_shared_window = NULL;
            g_sdl_shared_window_refs = 0;
        }
    }
    pthread_mutex_unlock(&g_sdl_window_mutex);

    if (!destroy) {
        LOGI("SDL_DestroyWindow: keeping shared window %p alive for the remaining aliases", window);
        return;
    }

    BYTEHOOK_CALL_PREV(
            custom_SDL_DestroyWindow_Func,
            SDL_DestroyWindow_t,
            window
    );

    BYTEHOOK_POP_STACK();
}

void create_sdl_hooks(bytehook_hook_all_t bytehook_hook_all_p) {
    // Don't set callee_path_name to anything besides NULL or else it won't be able to find the symbol
    bytehook_stub_t stub_SDL_InitSubSystem = bytehook_hook_all_p(NULL, "SDL_InitSubSystem", &custom_SDL_InitSubSystem_Func, NULL, NULL);
    bytehook_stub_t stub_SDL_OpenJoystick = bytehook_hook_all_p(NULL, "SDL_OpenJoystick", &custom_SDL_OpenJoystick_Func, NULL, NULL);
    bytehook_stub_t stub_SDL_OpenGamepad  = bytehook_hook_all_p(NULL, "SDL_OpenGamepad",  &custom_SDL_OpenGamepad_Func,  NULL, NULL);
    bytehook_stub_t stub_SDL_CloseJoystick = bytehook_hook_all_p(NULL, "SDL_CloseJoystick", &custom_SDL_CloseJoystick_Func, NULL, NULL);
    bytehook_stub_t stub_SDL_CloseGamepad  = bytehook_hook_all_p(NULL, "SDL_CloseGamepad",  &custom_SDL_CloseGamepad_Func,  NULL, NULL);
    bytehook_stub_t stub_SDL_LoadObject = bytehook_hook_all_p(NULL, "SDL_LoadObject", &custom_SDL_LoadObject_Func, NULL, NULL);
    bytehook_stub_t stub_SDL_CreateWindow = bytehook_hook_all_p(NULL, "SDL_CreateWindow", &custom_SDL_CreateWindow_Func, NULL, NULL);
    bytehook_stub_t stub_SDL_DestroyWindow = bytehook_hook_all_p(NULL, "SDL_DestroyWindow", &custom_SDL_DestroyWindow_Func, NULL, NULL);
    LOGI("Successfully initialized SDL hook, stub: %p\n", stub_SDL_InitSubSystem);
}
