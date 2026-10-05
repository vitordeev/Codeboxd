import React, { useContext, useMemo, useReducer, useRef, useState, createElement, useEffect, useLayoutEffect } from "react"
import { applyDelta, ReflexEvent, hydrateClientStorage, useEventLoop, refs } from "$/utils/state"
import { ColorModeContext, UploadFilesContext, DispatchContext, EventLoopContext, getStateContext, registerApp, eventLoop } from "$/utils/context-registry"
import { jsx } from "@emotion/react";

// Disable React dev-build owner-stack capture: the per-element Error()
// dominates dev-mode render CPU on large pages. Costs owner frames in
// `React.captureOwnerStack()`; set REFLEX_REACT_OWNER_STACKS=1 to restore.
// Full context: https://github.com/reflex-dev/reflex/pull/6905
if (typeof window !== "undefined") {
  try {
    const reactInternals =
      React.__CLIENT_INTERNALS_DO_NOT_USE_OR_WARN_USERS_THEY_CANNOT_UPGRADE;
    const ownerStackCounterKey = "recentlyCreatedOwnerStacks";
    if (
      reactInternals &&
      typeof reactInternals[ownerStackCounterKey] === "number"
    ) {
      Object.defineProperty(reactInternals, ownerStackCounterKey, {
        get: () => 1e9,
        set: () => {},
        configurable: true,
      });
    }
  } catch {}
}

export { ColorModeContext, UploadFilesContext, DispatchContext, EventLoopContext };
export const initialState = {"reflex___state____state": {"is_hydrated_rx_state_": false, "media_id_rx_state_": "", "profile_id_rx_state_": "", "rx_router_headers_rx_state_": {"host": "", "origin": "", "upgrade": "", "connection": "", "cookie": "", "pragma": "", "cache_control": "", "user_agent": "", "sec_websocket_version": "", "sec_websocket_key": "", "sec_websocket_extensions": "", "accept_encoding": "", "accept_language": "", "raw_headers": {}}, "rx_router_page_rx_state_": {"host": "", "path": "", "raw_path": "", "full_path": "", "full_raw_path": "", "params": {}}, "rx_router_route_id_rx_state_": "", "rx_router_session_rx_state_": {"client_token": "", "client_ip": "", "session_id": ""}, "rx_router_url_rx_state_": {"scheme": "", "netloc": "", "origin": "://", "path": "", "query": "", "query_parameters": {}, "fragment": "", "href": ""}}, "reflex___state____state.codeboxd_main____codeboxd_main____state": {}, "reflex___state____state.codeboxd_main___state___session____session_state": {"admin_password_visible_rx_state_": false, "auth_token_rx_state_": "", "error_message_rx_state_": "", "is_admin_rx_state_": false, "is_authenticated_rx_state_": false, "is_loading_rx_state_": false, "reset_message_rx_state_": "", "reset_success_rx_state_": false, "session_token_rx_state_": "", "user_id_rx_state_": 0, "user_name_rx_state_": "", "user_role_rx_state_": ""}, "reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___admin____admin_state": {"catalog_create_loading_rx_state_": false, "catalog_edit_cover_rx_state_": "", "catalog_edit_description_rx_state_": "", "catalog_edit_id_rx_state_": "", "catalog_edit_loading_rx_state_": false, "catalog_edit_title_rx_state_": "", "catalog_edit_year_rx_state_": "", "catalog_error_rx_state_": "", "catalog_items_rx_state_": [], "catalog_loading_rx_state_": false, "catalog_next_page_rx_state_": 0, "catalog_notice_rx_state_": "", "catalog_page_rx_state_": 1, "catalog_query_rx_state_": "", "catalog_total_rx_state_": 0, "catalog_type_rx_state_": "movie", "dashboard_error_rx_state_": "", "dashboard_loading_rx_state_": false, "dashboard_stats_rx_state_": {"users_total": "—", "posts_total": "—", "media_total": "—", "reports_pending": "—"}, "dashboard_updated_at_rx_state_": "", "pending_reports_rx_state_": [], "recent_posts_rx_state_": [], "report_review_decision_rx_state_": "", "report_review_id_rx_state_": "", "report_review_loading_rx_state_": false, "report_review_status_rx_state_": "", "reports_rx_state_": [], "reports_error_rx_state_": "", "reports_loading_rx_state_": false, "reports_next_page_rx_state_": 0, "reports_notice_rx_state_": "", "reports_page_rx_state_": 1, "reports_reason_filter_rx_state_": "", "reports_status_filter_rx_state_": "pending", "reports_total_rx_state_": 0, "reports_type_filter_rx_state_": "", "user_action_id_rx_state_": "", "user_action_loading_rx_state_": false, "user_action_reason_rx_state_": "", "user_action_status_rx_state_": "", "user_details_id_rx_state_": "", "users_rx_state_": [], "users_error_rx_state_": "", "users_loading_rx_state_": false, "users_next_page_rx_state_": 0, "users_notice_rx_state_": "", "users_page_rx_state_": 1, "users_query_rx_state_": "", "users_role_filter_rx_state_": "", "users_status_filter_rx_state_": "", "users_total_rx_state_": 0}, "reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state": {"availability_rx_state_": [], "busy_rx_state_": false, "catalog_items_rx_state_": [], "comments_rx_state_": [], "community_reviews_rx_state_": [], "edit_comment_body_rx_state_": "", "edit_comment_id_rx_state_": "", "edit_post_body_rx_state_": "", "edit_post_id_rx_state_": "", "edit_post_media_rx_state_": "0", "edit_post_spoiler_rx_state_": false, "failed_covers_rx_state_": [], "featured_items_rx_state_": [], "followers_rx_state_": [], "following_rx_state_": [], "following_ids_rx_state_": [], "guest_ratings_rx_state_": "{}", "has_more_results_rx_state_": true, "home_collection_errors_rx_state_": [], "home_collections_rx_state_": {"movies_now": [], "movies_rated": [], "movies_upcoming": [], "series_rated": [], "books_fiction": [], "books_fantasy": [], "books_mystery": [], "books_popular": [], "books_game_theory": [], "anime_rated": [], "anime_popular": [], "anime_current": []}, "home_loaded_rx_state_": false, "library_rx_state_": [], "liked_posts_rx_state_": [], "list_editor_open_rx_state_": false, "list_items_rx_state_": [], "lists_rx_state_": [], "notice_rx_state_": "", "owns_list_rx_state_": false, "owns_profile_rx_state_": false, "people_rx_state_": [], "popular_exhausted_rx_state_": [], "popular_movies_rx_state_": [], "popular_series_rx_state_": [], "post_editor_open_rx_state_": false, "post_existing_image_url_rx_state_": "", "post_image_filename_rx_state_": "", "post_image_mime_rx_state_": "", "post_media_query_rx_state_": "", "post_media_results_rx_state_": [], "post_media_searching_rx_state_": false, "post_media_selected_rx_state_": {"id": "", "key": "", "title": "", "cover": ""}, "post_saving_rx_state_": false, "posts_rx_state_": [], "profile_rx_state_": {"user_id": "", "username": "", "display_name": "", "bio": "", "avatar_url": "", "banner_url": ""}, "profile_activity_rx_state_": [], "profile_stats_rx_state_": "", "quick_lists_rx_state_": [], "recommendations_rx_state_": [], "report_description_rx_state_": "", "report_dialog_open_rx_state_": false, "report_reason_rx_state_": "spam", "report_sending_rx_state_": false, "report_target_id_rx_state_": "", "report_target_type_rx_state_": "", "search_active_rx_state_": false, "search_page_rx_state_": 1, "search_results_rx_state_": [], "search_term_rx_state_": "", "search_type_rx_state_": "all", "selected_rx_state_": {"id": "", "title": "", "kind": "", "year": "", "cover": "", "description": "", "details": "", "source": "", "external_id": "", "backdrop": ""}, "selected_list_rx_state_": {"id": "", "title": "", "description": "", "user_id": "", "is_public": "True"}, "selected_post_rx_state_": "", "selected_rating_rx_state_": "0", "selected_review_rx_state_": "", "selected_spoiler_rx_state_": false, "selected_status_rx_state_": "planned", "submitted_query_rx_state_": "", "suggested_people_rx_state_": [], "trailers_rx_state_": [], "visible_count_rx_state_": 20, "visible_library_rx_state_": [], "visible_lists_rx_state_": [], "visible_people_rx_state_": [], "visible_posts_rx_state_": []}, "reflex___state____state.reflex___istate___shared____shared_state_base_internal": {}, "reflex___state____state.reflex___state____frontend_event_exception_state": {}, "reflex___state____state.reflex___state____on_load_internal_state": {}, "reflex___state____state.reflex___state____update_vars_internal_state": {}}

export const defaultColorMode = "system"
export const StateContexts = {reflex___state____state: getStateContext("reflex___state____state"),reflex___state____state__codeboxd_main____codeboxd_main____state: getStateContext("reflex___state____state.codeboxd_main____codeboxd_main____state"),reflex___state____state__codeboxd_main___state___session____session_state: getStateContext("reflex___state____state.codeboxd_main___state___session____session_state"),reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state: getStateContext("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___admin____admin_state"),reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state: getStateContext("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state"),reflex___state____state__reflex___istate___shared____shared_state_base_internal: getStateContext("reflex___state____state.reflex___istate___shared____shared_state_base_internal"),reflex___state____state__reflex___state____frontend_event_exception_state: getStateContext("reflex___state____state.reflex___state____frontend_event_exception_state"),reflex___state____state__reflex___state____on_load_internal_state: getStateContext("reflex___state____state.reflex___state____on_load_internal_state"),reflex___state____state__reflex___state____update_vars_internal_state: getStateContext("reflex___state____state.reflex___state____update_vars_internal_state"),};
export const clientStorage = {"cookies": {"reflex___state____state.codeboxd_main___state___session____session_state.auth_token_rx_state_": {"name": "codeboxd_auth", "path": "/", "maxAge": 86400, "secure": false, "sameSite": "lax"}}, "local_storage": {"reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.guest_ratings_rx_state_": {"name": "codeboxd_guest_ratings", "sync": true}}, "session_storage": {"reflex___state____state.codeboxd_main___state___session____session_state.session_token_rx_state_": {"name": "codeboxd_session"}}}


export const state_name = "reflex___state____state"

export const exception_state_name = "reflex___state____state.reflex___state____frontend_event_exception_state"

// These events are triggered on initial load and each page navigation.
export const onLoadInternalEvent = () => {
    const internal_events = [];

    // Get tracked cookie and local storage vars to send to the backend.
    const client_storage_vars = hydrateClientStorage(clientStorage);
    // But only send the vars if any are actually set in the browser.
    if (client_storage_vars && Object.keys(client_storage_vars).length !== 0) {
        internal_events.push(
            ReflexEvent(
                'reflex___state____state.reflex___state____update_vars_internal_state.update_vars_internal',
                {vars: client_storage_vars},
            ),
        );
    }

    // `on_load_internal` triggers the correct on_load event(s) for the current page.
    // If the page does not define any on_load event, this will just set `is_hydrated = true`.
    internal_events.push(ReflexEvent('reflex___state____state.reflex___state____on_load_internal_state.on_load_internal'));

    return internal_events;
}

// The following events are sent when the websocket connects or reconnects.
export const initialEvents = () => [
    ReflexEvent('reflex___state____state.hydrate'),
    ...onLoadInternalEvent()
]
    

export const isDevMode = true;

// The static runtime reads these through the registry, so this module is the
// only one Vite re-executes when they change.
registerApp({
  initialState,
  clientStorage,
  state_name,
  exception_state_name,
  onLoadInternalEvent,
  initialEvents,
  isDevMode,
  defaultColorMode,
});

export function addEvents(events, args, event_actions) {
  return eventLoop.addEvents(events, args, event_actions);
}

export function getConnectErrors() {
  return eventLoop.connectErrors;
}

export function UploadFilesProvider({ children }) {
  const [filesById, setFilesById] = useState({})
  refs["__clear_selected_files"] = (id) => setFilesById(filesById => {
    const newFilesById = {...filesById}
    delete newFilesById[id]
    return newFilesById
  })
  return createElement(
    UploadFilesContext.Provider,
    { value: [filesById, setFilesById] },
    children
  );
}

// ``displayName`` is what React DevTools shows for the wrapper; without it
// every client-only component in the tree renders as ``Anonymous``.
export function ClientSide(component, name) {
  function ClientSideComponent({ children, ...props }) {
    const [Component, setComponent] = useState(null);
    useEffect(() => {
      async function load() {
        const comp = await component();
        setComponent(() => comp);
      }
      load();
    }, []);
    return Component ? jsx(Component, props, children) : null;
  }
  ClientSideComponent.displayName = name ? `ClientSide(${name})` : "ClientSide";
  return ClientSideComponent;
}

export function EventLoopProvider({ children }) {
  const dispatch = useContext(DispatchContext)
  const [addEventsLocal, connectErrors] = useEventLoop(
    dispatch,
    initialEvents,
    clientStorage,
  )
  // Publish the dispatchers so JSX literals constructed outside the
  // React-tree path (e.g. ``ErrorBoundary.onError``) can call ``addEvents``.
  eventLoop.addEvents = addEventsLocal;
  eventLoop.connectErrors = connectErrors;
  return useMemo(
    () =>
      createElement(
        EventLoopContext.Provider,
        { value: [addEventsLocal, connectErrors] },
        children
      ),
    [addEventsLocal, connectErrors, children],
  );
}

// ``useLayoutEffect`` warns when rendered on the server, where no effect runs
// at all, so fall back to ``useEffect`` there.
const useIsomorphicLayoutEffect =
  typeof document !== "undefined" ? useLayoutEffect : useEffect;

// Holds the mutable substate -> dispatch registry that ``SubstateProvider``
// writes into and ``EventLoopProvider`` reads. The registry object identity is
// stable for the lifetime of the tree, so neither adding a dispatcher nor
// updating a substate re-renders the consumers of ``DispatchContext``.
const DispatchProvider = ({ children }) => {
  const dispatchers = useRef({});
  return useMemo(
    () =>
      createElement(DispatchContext, { value: dispatchers.current }, children),
    [children],
  );
};

// One provider per substate: each owns its own reducer, so a delta for one
// substate only re-renders its provider instead of recreating every provider.
const SubstateProvider = ({ children, substateName, contextName }) => {
  const dispatchers = useContext(DispatchContext);
  const [state, dispatchSubstate] = useReducer(
    applyDelta,
    initialState[substateName],
  );
  // A layout effect, not a passive one: layout effects for the whole commit
  // run before any passive effect, so every dispatcher is registered before
  // ``EventLoopProvider`` (mounted below this provider) connects the socket.
  // A delta naming an unregistered substate is a fatal state mismatch.
  useIsomorphicLayoutEffect(() => {
    dispatchers[substateName] = dispatchSubstate;
    return () => {
      delete dispatchers[substateName];
    };
  }, [dispatchers, dispatchSubstate, substateName]);
  return useMemo(
    () => createElement(StateContexts[contextName], { value: state }, children),
    [children, state, contextName],
  );
};

export function StateProvider({ children }) {
  return useMemo(
    () => (
    createElement(DispatchProvider, {},
    createElement(SubstateProvider, {substateName: 'reflex___state____state', contextName: 'reflex___state____state'},
createElement(SubstateProvider, {substateName: 'reflex___state____state.codeboxd_main____codeboxd_main____state', contextName: 'reflex___state____state__codeboxd_main____codeboxd_main____state'},
createElement(SubstateProvider, {substateName: 'reflex___state____state.codeboxd_main___state___session____session_state', contextName: 'reflex___state____state__codeboxd_main___state___session____session_state'},
createElement(SubstateProvider, {substateName: 'reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___admin____admin_state', contextName: 'reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state'},
createElement(SubstateProvider, {substateName: 'reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state', contextName: 'reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state'},
createElement(SubstateProvider, {substateName: 'reflex___state____state.reflex___istate___shared____shared_state_base_internal', contextName: 'reflex___state____state__reflex___istate___shared____shared_state_base_internal'},
createElement(SubstateProvider, {substateName: 'reflex___state____state.reflex___state____frontend_event_exception_state', contextName: 'reflex___state____state__reflex___state____frontend_event_exception_state'},
createElement(SubstateProvider, {substateName: 'reflex___state____state.reflex___state____on_load_internal_state', contextName: 'reflex___state____state__reflex___state____on_load_internal_state'},
createElement(SubstateProvider, {substateName: 'reflex___state____state.reflex___state____update_vars_internal_state', contextName: 'reflex___state____state__reflex___state____update_vars_internal_state'},children
    )))))))))
  )),
    [children],
  );
}