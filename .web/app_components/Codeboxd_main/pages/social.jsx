
import {ReflexEvent,applyEventActions,getBackendURL,getRefValue,getRefValues,isNotNullOrUndefined,isTrue,mergeSlotProps,pyAnd,pyOr,refs} from "$/utils/state"
import {Link as ReactRouterLink} from "react-router"
import {StateContexts,UploadFilesContext,addEvents} from "$/utils/context"
import {Fragment,memo,useCallback,useContext,useEffect,useRef} from "react"
import {jsx} from "@emotion/react"
import {} from "react-dropzone"
import {useDropzone} from "react-dropzone"
import LucideImageUp from "lucide-react/dist/esm/icons/image-up.mjs"
import LucideBookOpen from "lucide-react/dist/esm/icons/book-open.mjs"
import LucideClapperboard from "lucide-react/dist/esm/icons/clapperboard.mjs"
import LucideUserRound from "lucide-react/dist/esm/icons/user-round.mjs"
import LucideHeart from "lucide-react/dist/esm/icons/heart.mjs"
import LucideMessageCircle from "lucide-react/dist/esm/icons/message-circle.mjs"
import LucideListVideo from "lucide-react/dist/esm/icons/list-video.mjs"
import LucideChevronRight from "lucide-react/dist/esm/icons/chevron-right.mjs"
import env from "$/env.json"
import {AlertDialog as RadixThemesAlertDialog,Button as RadixThemesButton,Dialog as RadixThemesDialog,Flex as RadixThemesFlex} from "@radix-ui/themes"








export const Reactrouterlink_link_89ecf437dde06100e9ef22e036f7f721_3e8caf1e = /*#__PURE__*/ (() => {
const Reactrouterlink_link_89ecf437dde06100e9ef22e036f7f721_3e8caf1e = memo(({children, ...rest}) => {
    const reflex___state____state = useContext(StateContexts.reflex___state____state)



    return(
        jsx(ReactRouterLink,{...mergeSlotProps(rest, ({ className:((reflex___state____state.rx_router_url_rx_state_?.["path"]?.valueOf?.() === "/"?.valueOf?.()) ? "nav-link active" : "nav-link"), to:"/" }))},children)
    )
});
Reactrouterlink_link_89ecf437dde06100e9ef22e036f7f721_3e8caf1e.displayName = "ReactRouterLink";
return Reactrouterlink_link_89ecf437dde06100e9ef22e036f7f721_3e8caf1e;
})();

export const Reactrouterlink_link_dfcc8a8f5c2fd192e886f24a88dbd7a5_3e8caf1e = /*#__PURE__*/ (() => {
const Reactrouterlink_link_dfcc8a8f5c2fd192e886f24a88dbd7a5_3e8caf1e = memo(({children, ...rest}) => {
    const reflex___state____state = useContext(StateContexts.reflex___state____state)



    return(
        jsx(ReactRouterLink,{...mergeSlotProps(rest, ({ className:((reflex___state____state.rx_router_url_rx_state_?.["path"]?.valueOf?.() === "/feed"?.valueOf?.()) ? "nav-link active" : "nav-link"), to:"/feed" }))},children)
    )
});
Reactrouterlink_link_dfcc8a8f5c2fd192e886f24a88dbd7a5_3e8caf1e.displayName = "ReactRouterLink";
return Reactrouterlink_link_dfcc8a8f5c2fd192e886f24a88dbd7a5_3e8caf1e;
})();

export const Reactrouterlink_link_47acbcabec187c0b2d9c67693763ae18_3e8caf1e = /*#__PURE__*/ (() => {
const Reactrouterlink_link_47acbcabec187c0b2d9c67693763ae18_3e8caf1e = memo(({children, ...rest}) => {
    const reflex___state____state = useContext(StateContexts.reflex___state____state)



    return(
        jsx(ReactRouterLink,{...mergeSlotProps(rest, ({ className:((reflex___state____state.rx_router_url_rx_state_?.["path"]?.valueOf?.() === "/listas"?.valueOf?.()) ? "nav-link active" : "nav-link"), to:"/listas" }))},children)
    )
});
Reactrouterlink_link_47acbcabec187c0b2d9c67693763ae18_3e8caf1e.displayName = "ReactRouterLink";
return Reactrouterlink_link_47acbcabec187c0b2d9c67693763ae18_3e8caf1e;
})();

export const Reactrouterlink_link_f854b28ce4f351bff2073301e61e4752_3e8caf1e = /*#__PURE__*/ (() => {
const Reactrouterlink_link_f854b28ce4f351bff2073301e61e4752_3e8caf1e = memo(({children, ...rest}) => {
    const reflex___state____state = useContext(StateContexts.reflex___state____state)



    return(
        jsx(ReactRouterLink,{...mergeSlotProps(rest, ({ className:((reflex___state____state.rx_router_url_rx_state_?.["path"]?.valueOf?.() === "/conta"?.valueOf?.()) ? "nav-link active" : "nav-link"), to:"/conta" }))},children)
    )
});
Reactrouterlink_link_f854b28ce4f351bff2073301e61e4752_3e8caf1e.displayName = "ReactRouterLink";
return Reactrouterlink_link_f854b28ce4f351bff2073301e61e4752_3e8caf1e;
})();

export const Button_button_da6062c13d4e2d445340661abe7b25db_3e8caf1e = /*#__PURE__*/ (() => {
const Button_button_da6062c13d4e2d445340661abe7b25db_3e8caf1e = memo(({children, ...rest}) => {
    const on_click_c6cae790485c63f5e2efc828e431c884 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.logout_social", ({  }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])



    return(
        jsx("button",{...mergeSlotProps(rest, ({ className:"action-button", onClick:on_click_c6cae790485c63f5e2efc828e431c884, type:"button" }))},children)
    )
});
Button_button_da6062c13d4e2d445340661abe7b25db_3e8caf1e.displayName = "Button";
return Button_button_da6062c13d4e2d445340661abe7b25db_3e8caf1e;
})();

export const Cond_comp_6d8cd40257ffb77da1c8b3a37595687b_3e8caf1e = /*#__PURE__*/ (() => {
const Cond_comp_6d8cd40257ffb77da1c8b3a37595687b_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state)



    return(
        (reflex___state____state__codeboxd_main___state___session____session_state.is_authenticated_rx_state_?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_6d8cd40257ffb77da1c8b3a37595687b_3e8caf1e.displayName = "Cond";
return Cond_comp_6d8cd40257ffb77da1c8b3a37595687b_3e8caf1e;
})();

export const Bare_comp_6983099407c8f808af6b67139eb88726_3e8caf1e = /*#__PURE__*/ (() => {
const Bare_comp_6983099407c8f808af6b67139eb88726_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.notice_rx_state_
    )
});
Bare_comp_6983099407c8f808af6b67139eb88726_3e8caf1e.displayName = "Bare";
return Bare_comp_6983099407c8f808af6b67139eb88726_3e8caf1e;
})();

export const Cond_comp_6e8e1e8992da03e265db6d4715b13170_3e8caf1e = /*#__PURE__*/ (() => {
const Cond_comp_6e8e1e8992da03e265db6d4715b13170_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        (!((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.notice_rx_state_?.valueOf?.() === ""?.valueOf?.()))?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_6e8e1e8992da03e265db6d4715b13170_3e8caf1e.displayName = "Cond";
return Cond_comp_6e8e1e8992da03e265db6d4715b13170_3e8caf1e;
})();

export const Cond_comp_3870c9193484052b2aa2a8daf28c5b57_3e8caf1e = /*#__PURE__*/ (() => {
const Cond_comp_3870c9193484052b2aa2a8daf28c5b57_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        (reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.busy_rx_state_?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_3870c9193484052b2aa2a8daf28c5b57_3e8caf1e.displayName = "Cond";
return Cond_comp_3870c9193484052b2aa2a8daf28c5b57_3e8caf1e;
})();

export const Input_input_8553451fd813c348631d11b951b12037_3e8caf1e = /*#__PURE__*/ (() => {
const Input_input_8553451fd813c348631d11b951b12037_3e8caf1e = memo(({children, ...rest}) => {
    const on_change_a2ed309d1251c6194d599a3466ab7958 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.update_search_term", ({ ["value"] : _e?.["target"]?.["value"] }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])
const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        jsx("input",{...mergeSlotProps(rest, ({ "aria-label":"Buscar t\u00edtulo", maxLength:200, name:"query", onChange:on_change_a2ed309d1251c6194d599a3466ab7958, placeholder:"Pesquisar filmes, s\u00e9ries, animes e livros", value:(isNotNullOrUndefined(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.search_term_rx_state_) ? reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.search_term_rx_state_ : "") }))},)
    )
});
Input_input_8553451fd813c348631d11b951b12037_3e8caf1e.displayName = "Input";
return Input_input_8553451fd813c348631d11b951b12037_3e8caf1e;
})();

export const Button_button_81ae41044f96899ead719aad2c79e6c5_3e8caf1e = /*#__PURE__*/ (() => {
const Button_button_81ae41044f96899ead719aad2c79e6c5_3e8caf1e = memo(({children, ...rest}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        jsx("button",{...mergeSlotProps(rest, ({ className:"action-button", disabled:reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.busy_rx_state_, type:"submit" }))},children)
    )
});
Button_button_81ae41044f96899ead719aad2c79e6c5_3e8caf1e.displayName = "Button";
return Button_button_81ae41044f96899ead719aad2c79e6c5_3e8caf1e;
})();

export const Form_form_644acc5f2355f7230548c8883c404fab_3e8caf1e = /*#__PURE__*/ (() => {
const Form_form_644acc5f2355f7230548c8883c404fab_3e8caf1e = memo(({children, ...rest}) => {
    

    const handleSubmit_c9645c1cb4812d991e7c3ac916c7fa82 = useCallback((ev) => {
        const $form = ev.target
        ev.preventDefault()
        const form_data = {...Object.fromEntries(new FormData($form).entries()), ...({  })};

        (((...args) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.search", ({ ["form"] : form_data }), ({  })))], args, ({  }))))(ev));

        if (false) {
            $form.reset()
        }
    })
    


    return(
        jsx("form",{...mergeSlotProps(rest, ({ className:"space-y-7", onSubmit:handleSubmit_c9645c1cb4812d991e7c3ac916c7fa82 }))},children)
    )
});
Form_form_644acc5f2355f7230548c8883c404fab_3e8caf1e.displayName = "Form";
return Form_form_644acc5f2355f7230548c8883c404fab_3e8caf1e;
})();

export const Button_button_764bb62018fc15741be9d97ef544ab98_3e8caf1e = /*#__PURE__*/ (() => {
const Button_button_764bb62018fc15741be9d97ef544ab98_3e8caf1e = memo(({children, ...rest}) => {
    const on_click_2f6e1f9036ef4d95db9d621bf857af64 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.browse_category", ({ ["kind"] : "all" }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])
const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        jsx("button",{...mergeSlotProps(rest, ({ "aria-pressed":pyAnd(pyAnd(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.search_active_rx_state_, () => ((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.submitted_query_rx_state_?.valueOf?.() === ""?.valueOf?.()))), () => ((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.search_type_rx_state_?.valueOf?.() === "all"?.valueOf?.()))), className:"browse-category", disabled:reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.busy_rx_state_, onClick:on_click_2f6e1f9036ef4d95db9d621bf857af64, type:"button" }))},children)
    )
});
Button_button_764bb62018fc15741be9d97ef544ab98_3e8caf1e.displayName = "Button";
return Button_button_764bb62018fc15741be9d97ef544ab98_3e8caf1e;
})();

export const Button_button_53701fee317b135c384b9f0fba755d5d_3e8caf1e = /*#__PURE__*/ (() => {
const Button_button_53701fee317b135c384b9f0fba755d5d_3e8caf1e = memo(({children, ...rest}) => {
    const on_click_ef57eec1710b663637da459f3b0d6098 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.browse_category", ({ ["kind"] : "movie" }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])
const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        jsx("button",{...mergeSlotProps(rest, ({ "aria-pressed":pyAnd(pyAnd(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.search_active_rx_state_, () => ((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.submitted_query_rx_state_?.valueOf?.() === ""?.valueOf?.()))), () => ((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.search_type_rx_state_?.valueOf?.() === "movie"?.valueOf?.()))), className:"browse-category", disabled:reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.busy_rx_state_, onClick:on_click_ef57eec1710b663637da459f3b0d6098, type:"button" }))},children)
    )
});
Button_button_53701fee317b135c384b9f0fba755d5d_3e8caf1e.displayName = "Button";
return Button_button_53701fee317b135c384b9f0fba755d5d_3e8caf1e;
})();

export const Button_button_fb6bc486abcb833864d31b4c8bbcc40a_3e8caf1e = /*#__PURE__*/ (() => {
const Button_button_fb6bc486abcb833864d31b4c8bbcc40a_3e8caf1e = memo(({children, ...rest}) => {
    const on_click_398295c1d2dc80022950f902a097a926 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.browse_category", ({ ["kind"] : "anime" }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])
const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        jsx("button",{...mergeSlotProps(rest, ({ "aria-pressed":pyAnd(pyAnd(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.search_active_rx_state_, () => ((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.submitted_query_rx_state_?.valueOf?.() === ""?.valueOf?.()))), () => ((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.search_type_rx_state_?.valueOf?.() === "anime"?.valueOf?.()))), className:"browse-category", disabled:reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.busy_rx_state_, onClick:on_click_398295c1d2dc80022950f902a097a926, type:"button" }))},children)
    )
});
Button_button_fb6bc486abcb833864d31b4c8bbcc40a_3e8caf1e.displayName = "Button";
return Button_button_fb6bc486abcb833864d31b4c8bbcc40a_3e8caf1e;
})();

export const Button_button_72758b1eaf4e826ff9dd1cbbbe164204_3e8caf1e = /*#__PURE__*/ (() => {
const Button_button_72758b1eaf4e826ff9dd1cbbbe164204_3e8caf1e = memo(({children, ...rest}) => {
    const on_click_bb42b91543cd50f9ad779efc1e7c1843 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.browse_category", ({ ["kind"] : "series" }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])
const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        jsx("button",{...mergeSlotProps(rest, ({ "aria-pressed":pyAnd(pyAnd(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.search_active_rx_state_, () => ((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.submitted_query_rx_state_?.valueOf?.() === ""?.valueOf?.()))), () => ((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.search_type_rx_state_?.valueOf?.() === "series"?.valueOf?.()))), className:"browse-category", disabled:reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.busy_rx_state_, onClick:on_click_bb42b91543cd50f9ad779efc1e7c1843, type:"button" }))},children)
    )
});
Button_button_72758b1eaf4e826ff9dd1cbbbe164204_3e8caf1e.displayName = "Button";
return Button_button_72758b1eaf4e826ff9dd1cbbbe164204_3e8caf1e;
})();

export const Button_button_40ececdebecaa4a73c4dd864639cb1a9_3e8caf1e = /*#__PURE__*/ (() => {
const Button_button_40ececdebecaa4a73c4dd864639cb1a9_3e8caf1e = memo(({children, ...rest}) => {
    const on_click_4f598c473ba49203dcea18abed18d94b = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.browse_category", ({ ["kind"] : "book" }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])
const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        jsx("button",{...mergeSlotProps(rest, ({ "aria-pressed":pyAnd(pyAnd(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.search_active_rx_state_, () => ((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.submitted_query_rx_state_?.valueOf?.() === ""?.valueOf?.()))), () => ((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.search_type_rx_state_?.valueOf?.() === "book"?.valueOf?.()))), className:"browse-category", disabled:reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.busy_rx_state_, onClick:on_click_4f598c473ba49203dcea18abed18d94b, type:"button" }))},children)
    )
});
Button_button_40ececdebecaa4a73c4dd864639cb1a9_3e8caf1e.displayName = "Button";
return Button_button_40ececdebecaa4a73c4dd864639cb1a9_3e8caf1e;
})();

export const Button_button_e601ffd83a1b042e0209f388989547c5_3e8caf1e = /*#__PURE__*/ (() => {
const Button_button_e601ffd83a1b042e0209f388989547c5_3e8caf1e = memo(({children, ...rest}) => {
    const on_click_c5f9406221b6c4029113e9b358927357 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.show_home_catalog", ({  }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])



    return(
        jsx("button",{...mergeSlotProps(rest, ({ className:"quiet-button", onClick:on_click_c5f9406221b6c4029113e9b358927357, type:"button" }))},children)
    )
});
Button_button_e601ffd83a1b042e0209f388989547c5_3e8caf1e.displayName = "Button";
return Button_button_e601ffd83a1b042e0209f388989547c5_3e8caf1e;
})();

export const Cond_comp_b106529b06c107d0f00156535aa54da3_3e8caf1e = /*#__PURE__*/ (() => {
const Cond_comp_b106529b06c107d0f00156535aa54da3_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        (reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.search_active_rx_state_?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_b106529b06c107d0f00156535aa54da3_3e8caf1e.displayName = "Cond";
return Cond_comp_b106529b06c107d0f00156535aa54da3_3e8caf1e;
})();

export const Foreach_comp_7c651e36791c9fc9657b27e3e6e44435_3e8caf1e = /*#__PURE__*/ (() => {
const Foreach_comp_7c651e36791c9fc9657b27e3e6e44435_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        Array.prototype.map.call(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.featured_items_rx_state_.slice(undefined, 1) ?? [],((m_rx_state_,index_707b05d50268bab6a0e0bc6c6963752a)=>(jsx("article",{className:"home-spotlight",key:index_707b05d50268bab6a0e0bc6c6963752a},jsx(Fragment,{},(pyOr(pyAnd(!((m_rx_state_?.["backdrop"]?.valueOf?.() === ""?.valueOf?.())), () => (!(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.failed_covers_rx_state_.includes(m_rx_state_?.["backdrop"])))), () => (pyAnd(!((m_rx_state_?.["cover"]?.valueOf?.() === ""?.valueOf?.())), () => (!(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.failed_covers_rx_state_.includes(m_rx_state_?.["cover"]))))))?(jsx(Fragment,{},jsx("img",{alt:"",className:"spotlight-image",onError:((...args) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.cover_failed", ({ ["url"] : (pyAnd(!((m_rx_state_?.["backdrop"]?.valueOf?.() === ""?.valueOf?.())), () => (!(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.failed_covers_rx_state_.includes(m_rx_state_?.["backdrop"])))) ? m_rx_state_?.["backdrop"] : m_rx_state_?.["cover"]) }), ({  })))], args, ({  })))),src:(pyAnd(!((m_rx_state_?.["backdrop"]?.valueOf?.() === ""?.valueOf?.())), () => (!(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.failed_covers_rx_state_.includes(m_rx_state_?.["backdrop"])))) ? m_rx_state_?.["backdrop"] : m_rx_state_?.["cover"])},))):(jsx(Fragment,{},)))),jsx("div",{className:"spotlight-copy"},jsx("p",{className:"eyebrow"},"HOJE NO SEU RADAR"),jsx("p",{className:"spotlight-kicker"},"Uma pausa. Uma grande hist\u00f3ria."),jsx("h2",{className:"spotlight-title"},m_rx_state_?.["title"]),jsx("p",{className:"spotlight-meta"},((m_rx_state_?.["kind"]+" \u00b7 ")+m_rx_state_?.["year"])),jsx("p",{className:"spotlight-description"},m_rx_state_?.["description"]),jsx("div",{className:"spotlight-actions"},jsx("button",{className:"action-button",onClick:((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.open_featured", ({ ["source"] : m_rx_state_?.["source"], ["identifier"] : m_rx_state_?.["external_id"], ["kind"] : "movie" }), ({  })))], [_e], ({  })))),type:"button"},"Conhecer este filme"),jsx(ReactRouterLink,{className:"spotlight-secondary",to:"#home-filmes"},"Explorar cat\u00e1logo")))))))
    )
});
Foreach_comp_7c651e36791c9fc9657b27e3e6e44435_3e8caf1e.displayName = "Foreach";
return Foreach_comp_7c651e36791c9fc9657b27e3e6e44435_3e8caf1e;
})();

export const Cond_comp_8e6ab58860140b748eacd34aa40901b1_3e8caf1e = /*#__PURE__*/ (() => {
const Cond_comp_8e6ab58860140b748eacd34aa40901b1_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        (pyAnd(!(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.search_active_rx_state_), () => ((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.featured_items_rx_state_.length > 0)))?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_8e6ab58860140b748eacd34aa40901b1_3e8caf1e.displayName = "Cond";
return Cond_comp_8e6ab58860140b748eacd34aa40901b1_3e8caf1e;
})();

export const Bare_comp_9a0b098e3efd91ffb98312f502954b5a_3e8caf1e = /*#__PURE__*/ (() => {
const Bare_comp_9a0b098e3efd91ffb98312f502954b5a_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        (!((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.submitted_query_rx_state_?.valueOf?.() === ""?.valueOf?.())) ? "Resultados da busca" : "Explorar cat\u00e1logo")
    )
});
Bare_comp_9a0b098e3efd91ffb98312f502954b5a_3e8caf1e.displayName = "Bare";
return Bare_comp_9a0b098e3efd91ffb98312f502954b5a_3e8caf1e;
})();

export const Foreach_comp_cce223fa56f00c33d0283e4ea0773828_3e8caf1e = /*#__PURE__*/ (() => {
const Foreach_comp_cce223fa56f00c33d0283e4ea0773828_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        Array.prototype.map.call(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.search_results_rx_state_ ?? [],((m_rx_state_,index_d33269b22aebcb304da43c6d9d3fcb12)=>(jsx("button",{className:"media-card text-left",key:index_d33269b22aebcb304da43c6d9d3fcb12,onClick:((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.open_result", ({ ["key"] : m_rx_state_?.["key"] }), ({  })))], [_e], ({  })))),type:"button"},jsx("div",{className:"h-full"},jsx("div",{className:"cover-frame"},jsx("div",{"aria-hidden":true,className:"cover-placeholder"},jsx("span",{className:"cover-placeholder-brand"},"CODEBOXD"),jsx("div",{className:"cover-placeholder-copy"},jsx("span",{className:"cover-placeholder-label"},"Capa indispon\u00edvel"))),jsx(Fragment,{},(pyAnd(!((m_rx_state_?.["cover"]?.valueOf?.() === ""?.valueOf?.())), () => (!(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.failed_covers_rx_state_.includes(m_rx_state_?.["cover"]))))?(jsx(Fragment,{},jsx("img",{alt:m_rx_state_?.["title"],className:"media-cover",css:({ ["width"] : "100%", ["height"] : "100%" }),decoding:"async",loading:"lazy",onError:((...args) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.cover_failed", ({ ["url"] : m_rx_state_?.["cover"] }), ({  })))], args, ({  })))),src:m_rx_state_?.["cover"]},))):(jsx(Fragment,{},))))),jsx("div",{className:"p-4"},jsx("h3",{className:"font-semibold line-clamp-2"},m_rx_state_?.["title"]),jsx("p",{className:"text-sm text-gray-400 mt-3"},((m_rx_state_?.["kind"]+" \u00b7 ")+m_rx_state_?.["year"]))))))))
    )
});
Foreach_comp_cce223fa56f00c33d0283e4ea0773828_3e8caf1e.displayName = "Foreach";
return Foreach_comp_cce223fa56f00c33d0283e4ea0773828_3e8caf1e;
})();

export const Bare_comp_759b112b972e1da11a55f857659e20df_3e8caf1e = /*#__PURE__*/ (() => {
const Bare_comp_759b112b972e1da11a55f857659e20df_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state)



    return(
        (reflex___state____state__codeboxd_main___state___session____session_state.is_authenticated_rx_state_ ? "Minha biblioteca" : "Criar minha conta")
    )
});
Bare_comp_759b112b972e1da11a55f857659e20df_3e8caf1e.displayName = "Bare";
return Bare_comp_759b112b972e1da11a55f857659e20df_3e8caf1e;
})();

export const Reactrouterlink_link_c8101e7cd8f295127e34f20dddcebf22_3e8caf1e = /*#__PURE__*/ (() => {
const Reactrouterlink_link_c8101e7cd8f295127e34f20dddcebf22_3e8caf1e = memo(({children, ...rest}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state)



    return(
        jsx(ReactRouterLink,{...mergeSlotProps(rest, ({ className:"action-button", to:(reflex___state____state__codeboxd_main___state___session____session_state.is_authenticated_rx_state_ ? "/biblioteca" : "/cadastro") }))},children)
    )
});
Reactrouterlink_link_c8101e7cd8f295127e34f20dddcebf22_3e8caf1e.displayName = "ReactRouterLink";
return Reactrouterlink_link_c8101e7cd8f295127e34f20dddcebf22_3e8caf1e;
})();

export const Cond_comp_8ca887f9b398ea7c8625ccee41c6e96d_3e8caf1e = /*#__PURE__*/ (() => {
const Cond_comp_8ca887f9b398ea7c8625ccee41c6e96d_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        ((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.featured_items_rx_state_.length?.valueOf?.() === 0?.valueOf?.())?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_8ca887f9b398ea7c8625ccee41c6e96d_3e8caf1e.displayName = "Cond";
return Cond_comp_8ca887f9b398ea7c8625ccee41c6e96d_3e8caf1e;
})();

export const Button_button_cc4709d3665f7ae6a011a542de8acda3_3e8caf1e = /*#__PURE__*/ (() => {
const Button_button_cc4709d3665f7ae6a011a542de8acda3_3e8caf1e = memo(({children, ...rest}) => {
    const on_click_a559090071c1fdc327308c7d3134b72a = useCallback(((_e) => (addEvents([(ReflexEvent("_call_script", ({ ["javascript_code"] : "(() => { const row = document.getElementById('popular-movie');\n        if (row) row.scrollBy({left: row.clientWidth * .85 * -1,\n        behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth'}); })()", ["callback"] : null }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])



    return(
        jsx("button",{...mergeSlotProps(rest, ({ "aria-controls":"popular-movie", "aria-label":"Anteriores: Filmes populares", className:"shelf-arrow", onClick:on_click_a559090071c1fdc327308c7d3134b72a, type:"button" }))},children)
    )
});
Button_button_cc4709d3665f7ae6a011a542de8acda3_3e8caf1e.displayName = "Button";
return Button_button_cc4709d3665f7ae6a011a542de8acda3_3e8caf1e;
})();

export const Button_button_3c411238f8e7a3bda872c07768307823_3e8caf1e = /*#__PURE__*/ (() => {
const Button_button_3c411238f8e7a3bda872c07768307823_3e8caf1e = memo(({children, ...rest}) => {
    const on_click_dcd3640d6a6d2b1ff2e000df9d80da05 = useCallback(((_e) => (addEvents([(ReflexEvent("_call_script", ({ ["javascript_code"] : "(() => { const row = document.getElementById('popular-movie');\n        if (row) row.scrollBy({left: row.clientWidth * .85 * 1,\n        behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth'}); })()", ["callback"] : null }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])



    return(
        jsx("button",{...mergeSlotProps(rest, ({ "aria-controls":"popular-movie", "aria-label":"Pr\u00f3ximos: Filmes populares", className:"shelf-arrow", onClick:on_click_dcd3640d6a6d2b1ff2e000df9d80da05, type:"button" }))},children)
    )
});
Button_button_3c411238f8e7a3bda872c07768307823_3e8caf1e.displayName = "Button";
return Button_button_3c411238f8e7a3bda872c07768307823_3e8caf1e;
})();

export const Foreach_comp_acc9ea6a59ed9d65e8a0b891394ea1c6_3e8caf1e = /*#__PURE__*/ (() => {
const Foreach_comp_acc9ea6a59ed9d65e8a0b891394ea1c6_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        Array.prototype.map.call(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.popular_movies_rx_state_ ?? [],((m_rx_state_,index_rx_state_)=>(jsx("button",{className:"shelf-card",key:m_rx_state_?.["key"],onClick:((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.open_featured", ({ ["source"] : m_rx_state_?.["source"], ["identifier"] : m_rx_state_?.["external_id"], ["kind"] : "movie" }), ({  })))], [_e], ({  })))),type:"button"},jsx("div",{className:"shelf-poster"},jsx("div",{className:"cover-frame"},jsx("div",{"aria-hidden":true,className:"cover-placeholder"},jsx("span",{className:"cover-placeholder-brand"},"CODEBOXD"),jsx("div",{className:"cover-placeholder-copy"},jsx("span",{className:"cover-placeholder-label"},"Capa indispon\u00edvel"))),jsx(Fragment,{},(pyAnd(!((m_rx_state_?.["cover"]?.valueOf?.() === ""?.valueOf?.())), () => (!(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.failed_covers_rx_state_.includes(m_rx_state_?.["cover"]))))?(jsx(Fragment,{},jsx("img",{alt:m_rx_state_?.["title"],className:"media-cover",css:({ ["width"] : "100%", ["height"] : "100%" }),decoding:"async",loading:"lazy",onError:((...args) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.cover_failed", ({ ["url"] : m_rx_state_?.["cover"] }), ({  })))], args, ({  })))),src:m_rx_state_?.["cover"]},))):(jsx(Fragment,{},)))))),jsx("div",{className:"shelf-card-copy"},jsx("h3",{className:"shelf-card-title"},m_rx_state_?.["title"]),jsx("p",{className:"shelf-card-meta"},((m_rx_state_?.["kind"]+" \u00b7 ")+m_rx_state_?.["year"])))))))
    )
});
Foreach_comp_acc9ea6a59ed9d65e8a0b891394ea1c6_3e8caf1e.displayName = "Foreach";
return Foreach_comp_acc9ea6a59ed9d65e8a0b891394ea1c6_3e8caf1e;
})();

export const Button_button_a9fd0dfe8ac23c591c22d9aabf750612_3e8caf1e = /*#__PURE__*/ (() => {
const Button_button_a9fd0dfe8ac23c591c22d9aabf750612_3e8caf1e = memo(({children, ...rest}) => {
    const on_click_8e9f6ed1382956e8666e2258cadf7a6d = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.more_popular", ({ ["kind"] : "movie" }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])
const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        jsx("button",{...mergeSlotProps(rest, ({ className:"shelf-more", disabled:reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.busy_rx_state_, onClick:on_click_8e9f6ed1382956e8666e2258cadf7a6d, type:"button" }))},children)
    )
});
Button_button_a9fd0dfe8ac23c591c22d9aabf750612_3e8caf1e.displayName = "Button";
return Button_button_a9fd0dfe8ac23c591c22d9aabf750612_3e8caf1e;
})();

export const Cond_comp_53ba4e8a8c9aec838b16e2a4a0cf252a_3e8caf1e = /*#__PURE__*/ (() => {
const Cond_comp_53ba4e8a8c9aec838b16e2a4a0cf252a_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        (!(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.popular_exhausted_rx_state_.includes("movie"))?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_53ba4e8a8c9aec838b16e2a4a0cf252a_3e8caf1e.displayName = "Cond";
return Cond_comp_53ba4e8a8c9aec838b16e2a4a0cf252a_3e8caf1e;
})();

export const Cond_comp_1fc4d6dd2bc873e5aba221d48852eba4_3e8caf1e = /*#__PURE__*/ (() => {
const Cond_comp_1fc4d6dd2bc873e5aba221d48852eba4_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        ((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.popular_movies_rx_state_.length > 0)?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_1fc4d6dd2bc873e5aba221d48852eba4_3e8caf1e.displayName = "Cond";
return Cond_comp_1fc4d6dd2bc873e5aba221d48852eba4_3e8caf1e;
})();

export const Button_button_65e4a7d01c147f3d6d76bcc8cba7990d_3e8caf1e = /*#__PURE__*/ (() => {
const Button_button_65e4a7d01c147f3d6d76bcc8cba7990d_3e8caf1e = memo(({children, ...rest}) => {
    const on_click_1259c6d579c25b0c36a74ffae3d307e5 = useCallback(((_e) => (addEvents([(ReflexEvent("_call_script", ({ ["javascript_code"] : "(() => { const row = document.getElementById('movies_now');\n        if (row) row.scrollBy({left: row.clientWidth * .85 * -1,\n        behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth'}); })()", ["callback"] : null }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])



    return(
        jsx("button",{...mergeSlotProps(rest, ({ "aria-controls":"movies_now", "aria-label":"Anteriores: Agora nos cinemas", className:"shelf-arrow", onClick:on_click_1259c6d579c25b0c36a74ffae3d307e5, type:"button" }))},children)
    )
});
Button_button_65e4a7d01c147f3d6d76bcc8cba7990d_3e8caf1e.displayName = "Button";
return Button_button_65e4a7d01c147f3d6d76bcc8cba7990d_3e8caf1e;
})();

export const Button_button_66c8cdf3499bfcb5922b718cf98ab877_3e8caf1e = /*#__PURE__*/ (() => {
const Button_button_66c8cdf3499bfcb5922b718cf98ab877_3e8caf1e = memo(({children, ...rest}) => {
    const on_click_1bec5fc4f9c9aca8e73ba9dab451674a = useCallback(((_e) => (addEvents([(ReflexEvent("_call_script", ({ ["javascript_code"] : "(() => { const row = document.getElementById('movies_now');\n        if (row) row.scrollBy({left: row.clientWidth * .85 * 1,\n        behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth'}); })()", ["callback"] : null }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])



    return(
        jsx("button",{...mergeSlotProps(rest, ({ "aria-controls":"movies_now", "aria-label":"Pr\u00f3ximos: Agora nos cinemas", className:"shelf-arrow", onClick:on_click_1bec5fc4f9c9aca8e73ba9dab451674a, type:"button" }))},children)
    )
});
Button_button_66c8cdf3499bfcb5922b718cf98ab877_3e8caf1e.displayName = "Button";
return Button_button_66c8cdf3499bfcb5922b718cf98ab877_3e8caf1e;
})();

export const Foreach_comp_7d239bf1c95a466c2aecf4b1d999d442_3e8caf1e = /*#__PURE__*/ (() => {
const Foreach_comp_7d239bf1c95a466c2aecf4b1d999d442_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        Array.prototype.map.call(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.home_collections_rx_state_?.["movies_now"] ?? [],((m_rx_state_,index_rx_state_)=>(jsx("button",{className:"shelf-card",key:m_rx_state_?.["key"],onClick:((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.open_featured", ({ ["source"] : m_rx_state_?.["source"], ["identifier"] : m_rx_state_?.["external_id"], ["kind"] : "movie" }), ({  })))], [_e], ({  })))),type:"button"},jsx("div",{className:"shelf-poster"},jsx("div",{className:"cover-frame"},jsx("div",{"aria-hidden":true,className:"cover-placeholder"},jsx("span",{className:"cover-placeholder-brand"},"CODEBOXD"),jsx("div",{className:"cover-placeholder-copy"},jsx("span",{className:"cover-placeholder-label"},"Capa indispon\u00edvel"))),jsx(Fragment,{},(pyAnd(!((m_rx_state_?.["cover"]?.valueOf?.() === ""?.valueOf?.())), () => (!(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.failed_covers_rx_state_.includes(m_rx_state_?.["cover"]))))?(jsx(Fragment,{},jsx("img",{alt:m_rx_state_?.["title"],className:"media-cover",css:({ ["width"] : "100%", ["height"] : "100%" }),decoding:"async",loading:"lazy",onError:((...args) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.cover_failed", ({ ["url"] : m_rx_state_?.["cover"] }), ({  })))], args, ({  })))),src:m_rx_state_?.["cover"]},))):(jsx(Fragment,{},)))))),jsx("div",{className:"shelf-card-copy"},jsx("h3",{className:"shelf-card-title"},m_rx_state_?.["title"]),jsx("p",{className:"shelf-card-meta"},((m_rx_state_?.["kind"]+" \u00b7 ")+m_rx_state_?.["year"])))))))
    )
});
Foreach_comp_7d239bf1c95a466c2aecf4b1d999d442_3e8caf1e.displayName = "Foreach";
return Foreach_comp_7d239bf1c95a466c2aecf4b1d999d442_3e8caf1e;
})();

export const Bare_comp_3a7bdf68a5f9f25b75abce378f34f76b_3e8caf1e = /*#__PURE__*/ (() => {
const Bare_comp_3a7bdf68a5f9f25b75abce378f34f76b_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        (reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.home_collection_errors_rx_state_.includes("movies_now") ? "Esta sele\u00e7\u00e3o est\u00e1 indispon\u00edvel no momento." : "Ainda n\u00e3o h\u00e1 t\u00edtulos nesta sele\u00e7\u00e3o.")
    )
});
Bare_comp_3a7bdf68a5f9f25b75abce378f34f76b_3e8caf1e.displayName = "Bare";
return Bare_comp_3a7bdf68a5f9f25b75abce378f34f76b_3e8caf1e;
})();

export const Button_button_317bc80964bf4151d17e259452aec2fa_3e8caf1e = /*#__PURE__*/ (() => {
const Button_button_317bc80964bf4151d17e259452aec2fa_3e8caf1e = memo(({children, ...rest}) => {
    const on_click_77846084c957a81ab548234460010c62 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.retry_home_collections", ({  }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])
const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        jsx("button",{...mergeSlotProps(rest, ({ className:"quiet-button", disabled:reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.busy_rx_state_, onClick:on_click_77846084c957a81ab548234460010c62, type:"button" }))},children)
    )
});
Button_button_317bc80964bf4151d17e259452aec2fa_3e8caf1e.displayName = "Button";
return Button_button_317bc80964bf4151d17e259452aec2fa_3e8caf1e;
})();

export const Cond_comp_152e87f2a84885339a4b5d00c56375bf_3e8caf1e = /*#__PURE__*/ (() => {
const Cond_comp_152e87f2a84885339a4b5d00c56375bf_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        (!(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.home_loaded_rx_state_)?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_152e87f2a84885339a4b5d00c56375bf_3e8caf1e.displayName = "Cond";
return Cond_comp_152e87f2a84885339a4b5d00c56375bf_3e8caf1e;
})();

export const Cond_comp_09309529d8789d7ca0947e31a4981f78_3e8caf1e = /*#__PURE__*/ (() => {
const Cond_comp_09309529d8789d7ca0947e31a4981f78_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        ((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.home_collections_rx_state_?.["movies_now"].length > 0)?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_09309529d8789d7ca0947e31a4981f78_3e8caf1e.displayName = "Cond";
return Cond_comp_09309529d8789d7ca0947e31a4981f78_3e8caf1e;
})();

export const Button_button_db8059e3aee1c5c2316aaa7b4b9f6e10_3e8caf1e = /*#__PURE__*/ (() => {
const Button_button_db8059e3aee1c5c2316aaa7b4b9f6e10_3e8caf1e = memo(({children, ...rest}) => {
    const on_click_21cfbe510b7859bb5ed11e937d9fa17e = useCallback(((_e) => (addEvents([(ReflexEvent("_call_script", ({ ["javascript_code"] : "(() => { const row = document.getElementById('movies_rated');\n        if (row) row.scrollBy({left: row.clientWidth * .85 * -1,\n        behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth'}); })()", ["callback"] : null }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])



    return(
        jsx("button",{...mergeSlotProps(rest, ({ "aria-controls":"movies_rated", "aria-label":"Anteriores: Filmes muito bem avaliados", className:"shelf-arrow", onClick:on_click_21cfbe510b7859bb5ed11e937d9fa17e, type:"button" }))},children)
    )
});
Button_button_db8059e3aee1c5c2316aaa7b4b9f6e10_3e8caf1e.displayName = "Button";
return Button_button_db8059e3aee1c5c2316aaa7b4b9f6e10_3e8caf1e;
})();

export const Button_button_6d871c683fb9d4cc3f59c8518ee9b3d7_3e8caf1e = /*#__PURE__*/ (() => {
const Button_button_6d871c683fb9d4cc3f59c8518ee9b3d7_3e8caf1e = memo(({children, ...rest}) => {
    const on_click_8e49fb89d5dc451a2a181242237accb3 = useCallback(((_e) => (addEvents([(ReflexEvent("_call_script", ({ ["javascript_code"] : "(() => { const row = document.getElementById('movies_rated');\n        if (row) row.scrollBy({left: row.clientWidth * .85 * 1,\n        behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth'}); })()", ["callback"] : null }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])



    return(
        jsx("button",{...mergeSlotProps(rest, ({ "aria-controls":"movies_rated", "aria-label":"Pr\u00f3ximos: Filmes muito bem avaliados", className:"shelf-arrow", onClick:on_click_8e49fb89d5dc451a2a181242237accb3, type:"button" }))},children)
    )
});
Button_button_6d871c683fb9d4cc3f59c8518ee9b3d7_3e8caf1e.displayName = "Button";
return Button_button_6d871c683fb9d4cc3f59c8518ee9b3d7_3e8caf1e;
})();

export const Foreach_comp_8be33e04b26cb494fd721977d02367a0_3e8caf1e = /*#__PURE__*/ (() => {
const Foreach_comp_8be33e04b26cb494fd721977d02367a0_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        Array.prototype.map.call(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.home_collections_rx_state_?.["movies_rated"] ?? [],((m_rx_state_,index_rx_state_)=>(jsx("button",{className:"shelf-card",key:m_rx_state_?.["key"],onClick:((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.open_featured", ({ ["source"] : m_rx_state_?.["source"], ["identifier"] : m_rx_state_?.["external_id"], ["kind"] : "movie" }), ({  })))], [_e], ({  })))),type:"button"},jsx("div",{className:"shelf-poster"},jsx("div",{className:"cover-frame"},jsx("div",{"aria-hidden":true,className:"cover-placeholder"},jsx("span",{className:"cover-placeholder-brand"},"CODEBOXD"),jsx("div",{className:"cover-placeholder-copy"},jsx("span",{className:"cover-placeholder-label"},"Capa indispon\u00edvel"))),jsx(Fragment,{},(pyAnd(!((m_rx_state_?.["cover"]?.valueOf?.() === ""?.valueOf?.())), () => (!(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.failed_covers_rx_state_.includes(m_rx_state_?.["cover"]))))?(jsx(Fragment,{},jsx("img",{alt:m_rx_state_?.["title"],className:"media-cover",css:({ ["width"] : "100%", ["height"] : "100%" }),decoding:"async",loading:"lazy",onError:((...args) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.cover_failed", ({ ["url"] : m_rx_state_?.["cover"] }), ({  })))], args, ({  })))),src:m_rx_state_?.["cover"]},))):(jsx(Fragment,{},)))))),jsx("div",{className:"shelf-card-copy"},jsx("h3",{className:"shelf-card-title"},m_rx_state_?.["title"]),jsx("p",{className:"shelf-card-meta"},((m_rx_state_?.["kind"]+" \u00b7 ")+m_rx_state_?.["year"])))))))
    )
});
Foreach_comp_8be33e04b26cb494fd721977d02367a0_3e8caf1e.displayName = "Foreach";
return Foreach_comp_8be33e04b26cb494fd721977d02367a0_3e8caf1e;
})();

export const Bare_comp_e2b1c213499073ff3a2e6dd1f8cd341a_3e8caf1e = /*#__PURE__*/ (() => {
const Bare_comp_e2b1c213499073ff3a2e6dd1f8cd341a_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        (reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.home_collection_errors_rx_state_.includes("movies_rated") ? "Esta sele\u00e7\u00e3o est\u00e1 indispon\u00edvel no momento." : "Ainda n\u00e3o h\u00e1 t\u00edtulos nesta sele\u00e7\u00e3o.")
    )
});
Bare_comp_e2b1c213499073ff3a2e6dd1f8cd341a_3e8caf1e.displayName = "Bare";
return Bare_comp_e2b1c213499073ff3a2e6dd1f8cd341a_3e8caf1e;
})();

export const Cond_comp_d07cd6e158a92a61e18ea85ac0b8be13_3e8caf1e = /*#__PURE__*/ (() => {
const Cond_comp_d07cd6e158a92a61e18ea85ac0b8be13_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        ((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.home_collections_rx_state_?.["movies_rated"].length > 0)?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_d07cd6e158a92a61e18ea85ac0b8be13_3e8caf1e.displayName = "Cond";
return Cond_comp_d07cd6e158a92a61e18ea85ac0b8be13_3e8caf1e;
})();

export const Button_button_847798fe95f1416f9473c1251f162f1c_3e8caf1e = /*#__PURE__*/ (() => {
const Button_button_847798fe95f1416f9473c1251f162f1c_3e8caf1e = memo(({children, ...rest}) => {
    const on_click_2bc927baeec1fe6e32bf281710c48fa7 = useCallback(((_e) => (addEvents([(ReflexEvent("_call_script", ({ ["javascript_code"] : "(() => { const row = document.getElementById('movies_upcoming');\n        if (row) row.scrollBy({left: row.clientWidth * .85 * -1,\n        behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth'}); })()", ["callback"] : null }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])



    return(
        jsx("button",{...mergeSlotProps(rest, ({ "aria-controls":"movies_upcoming", "aria-label":"Anteriores: No radar: pr\u00f3ximos filmes", className:"shelf-arrow", onClick:on_click_2bc927baeec1fe6e32bf281710c48fa7, type:"button" }))},children)
    )
});
Button_button_847798fe95f1416f9473c1251f162f1c_3e8caf1e.displayName = "Button";
return Button_button_847798fe95f1416f9473c1251f162f1c_3e8caf1e;
})();

export const Button_button_a50b74937f0407ed15515af61eeee312_3e8caf1e = /*#__PURE__*/ (() => {
const Button_button_a50b74937f0407ed15515af61eeee312_3e8caf1e = memo(({children, ...rest}) => {
    const on_click_3d52607bb62a04cf24553729e35df1be = useCallback(((_e) => (addEvents([(ReflexEvent("_call_script", ({ ["javascript_code"] : "(() => { const row = document.getElementById('movies_upcoming');\n        if (row) row.scrollBy({left: row.clientWidth * .85 * 1,\n        behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth'}); })()", ["callback"] : null }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])



    return(
        jsx("button",{...mergeSlotProps(rest, ({ "aria-controls":"movies_upcoming", "aria-label":"Pr\u00f3ximos: No radar: pr\u00f3ximos filmes", className:"shelf-arrow", onClick:on_click_3d52607bb62a04cf24553729e35df1be, type:"button" }))},children)
    )
});
Button_button_a50b74937f0407ed15515af61eeee312_3e8caf1e.displayName = "Button";
return Button_button_a50b74937f0407ed15515af61eeee312_3e8caf1e;
})();

export const Foreach_comp_71f4a6c9739bfe908fc00a7e672eaaad_3e8caf1e = /*#__PURE__*/ (() => {
const Foreach_comp_71f4a6c9739bfe908fc00a7e672eaaad_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        Array.prototype.map.call(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.home_collections_rx_state_?.["movies_upcoming"] ?? [],((m_rx_state_,index_rx_state_)=>(jsx("button",{className:"shelf-card",key:m_rx_state_?.["key"],onClick:((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.open_featured", ({ ["source"] : m_rx_state_?.["source"], ["identifier"] : m_rx_state_?.["external_id"], ["kind"] : "movie" }), ({  })))], [_e], ({  })))),type:"button"},jsx("div",{className:"shelf-poster"},jsx("div",{className:"cover-frame"},jsx("div",{"aria-hidden":true,className:"cover-placeholder"},jsx("span",{className:"cover-placeholder-brand"},"CODEBOXD"),jsx("div",{className:"cover-placeholder-copy"},jsx("span",{className:"cover-placeholder-label"},"Capa indispon\u00edvel"))),jsx(Fragment,{},(pyAnd(!((m_rx_state_?.["cover"]?.valueOf?.() === ""?.valueOf?.())), () => (!(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.failed_covers_rx_state_.includes(m_rx_state_?.["cover"]))))?(jsx(Fragment,{},jsx("img",{alt:m_rx_state_?.["title"],className:"media-cover",css:({ ["width"] : "100%", ["height"] : "100%" }),decoding:"async",loading:"lazy",onError:((...args) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.cover_failed", ({ ["url"] : m_rx_state_?.["cover"] }), ({  })))], args, ({  })))),src:m_rx_state_?.["cover"]},))):(jsx(Fragment,{},)))))),jsx("div",{className:"shelf-card-copy"},jsx("h3",{className:"shelf-card-title"},m_rx_state_?.["title"]),jsx("p",{className:"shelf-card-meta"},((m_rx_state_?.["kind"]+" \u00b7 ")+m_rx_state_?.["year"])))))))
    )
});
Foreach_comp_71f4a6c9739bfe908fc00a7e672eaaad_3e8caf1e.displayName = "Foreach";
return Foreach_comp_71f4a6c9739bfe908fc00a7e672eaaad_3e8caf1e;
})();

export const Bare_comp_793a9e4e145ce2104b50fdac448acab8_3e8caf1e = /*#__PURE__*/ (() => {
const Bare_comp_793a9e4e145ce2104b50fdac448acab8_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        (reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.home_collection_errors_rx_state_.includes("movies_upcoming") ? "Esta sele\u00e7\u00e3o est\u00e1 indispon\u00edvel no momento." : "Ainda n\u00e3o h\u00e1 t\u00edtulos nesta sele\u00e7\u00e3o.")
    )
});
Bare_comp_793a9e4e145ce2104b50fdac448acab8_3e8caf1e.displayName = "Bare";
return Bare_comp_793a9e4e145ce2104b50fdac448acab8_3e8caf1e;
})();

export const Cond_comp_1cfec4d70bbd78c60bb1c5a7ed5b2120_3e8caf1e = /*#__PURE__*/ (() => {
const Cond_comp_1cfec4d70bbd78c60bb1c5a7ed5b2120_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        ((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.home_collections_rx_state_?.["movies_upcoming"].length > 0)?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_1cfec4d70bbd78c60bb1c5a7ed5b2120_3e8caf1e.displayName = "Cond";
return Cond_comp_1cfec4d70bbd78c60bb1c5a7ed5b2120_3e8caf1e;
})();

export const Button_button_e14f4591f71867b6d954c79254dc8d73_3e8caf1e = /*#__PURE__*/ (() => {
const Button_button_e14f4591f71867b6d954c79254dc8d73_3e8caf1e = memo(({children, ...rest}) => {
    const on_click_8e89d67d2fb919cabbdadca5cb3e5659 = useCallback(((_e) => (addEvents([(ReflexEvent("_call_script", ({ ["javascript_code"] : "(() => { const row = document.getElementById('popular-series');\n        if (row) row.scrollBy({left: row.clientWidth * .85 * -1,\n        behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth'}); })()", ["callback"] : null }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])



    return(
        jsx("button",{...mergeSlotProps(rest, ({ "aria-controls":"popular-series", "aria-label":"Anteriores: S\u00e9ries populares", className:"shelf-arrow", onClick:on_click_8e89d67d2fb919cabbdadca5cb3e5659, type:"button" }))},children)
    )
});
Button_button_e14f4591f71867b6d954c79254dc8d73_3e8caf1e.displayName = "Button";
return Button_button_e14f4591f71867b6d954c79254dc8d73_3e8caf1e;
})();

export const Button_button_0221bce1b4794fd7dd0f555aec0c4394_3e8caf1e = /*#__PURE__*/ (() => {
const Button_button_0221bce1b4794fd7dd0f555aec0c4394_3e8caf1e = memo(({children, ...rest}) => {
    const on_click_4cd9287f1a9036d6196e750f4198174f = useCallback(((_e) => (addEvents([(ReflexEvent("_call_script", ({ ["javascript_code"] : "(() => { const row = document.getElementById('popular-series');\n        if (row) row.scrollBy({left: row.clientWidth * .85 * 1,\n        behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth'}); })()", ["callback"] : null }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])



    return(
        jsx("button",{...mergeSlotProps(rest, ({ "aria-controls":"popular-series", "aria-label":"Pr\u00f3ximos: S\u00e9ries populares", className:"shelf-arrow", onClick:on_click_4cd9287f1a9036d6196e750f4198174f, type:"button" }))},children)
    )
});
Button_button_0221bce1b4794fd7dd0f555aec0c4394_3e8caf1e.displayName = "Button";
return Button_button_0221bce1b4794fd7dd0f555aec0c4394_3e8caf1e;
})();

export const Foreach_comp_9276ab616e083b61ffcab6f992efbb9e_3e8caf1e = /*#__PURE__*/ (() => {
const Foreach_comp_9276ab616e083b61ffcab6f992efbb9e_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        Array.prototype.map.call(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.popular_series_rx_state_ ?? [],((m_rx_state_,index_rx_state_)=>(jsx("button",{className:"shelf-card",key:m_rx_state_?.["key"],onClick:((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.open_featured", ({ ["source"] : m_rx_state_?.["source"], ["identifier"] : m_rx_state_?.["external_id"], ["kind"] : "series" }), ({  })))], [_e], ({  })))),type:"button"},jsx("div",{className:"shelf-poster"},jsx("div",{className:"cover-frame"},jsx("div",{"aria-hidden":true,className:"cover-placeholder"},jsx("span",{className:"cover-placeholder-brand"},"CODEBOXD"),jsx("div",{className:"cover-placeholder-copy"},jsx("span",{className:"cover-placeholder-label"},"Capa indispon\u00edvel"))),jsx(Fragment,{},(pyAnd(!((m_rx_state_?.["cover"]?.valueOf?.() === ""?.valueOf?.())), () => (!(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.failed_covers_rx_state_.includes(m_rx_state_?.["cover"]))))?(jsx(Fragment,{},jsx("img",{alt:m_rx_state_?.["title"],className:"media-cover",css:({ ["width"] : "100%", ["height"] : "100%" }),decoding:"async",loading:"lazy",onError:((...args) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.cover_failed", ({ ["url"] : m_rx_state_?.["cover"] }), ({  })))], args, ({  })))),src:m_rx_state_?.["cover"]},))):(jsx(Fragment,{},)))))),jsx("div",{className:"shelf-card-copy"},jsx("h3",{className:"shelf-card-title"},m_rx_state_?.["title"]),jsx("p",{className:"shelf-card-meta"},((m_rx_state_?.["kind"]+" \u00b7 ")+m_rx_state_?.["year"])))))))
    )
});
Foreach_comp_9276ab616e083b61ffcab6f992efbb9e_3e8caf1e.displayName = "Foreach";
return Foreach_comp_9276ab616e083b61ffcab6f992efbb9e_3e8caf1e;
})();

export const Button_button_07ddfc544246fcdba2120f7e6da99cc4_3e8caf1e = /*#__PURE__*/ (() => {
const Button_button_07ddfc544246fcdba2120f7e6da99cc4_3e8caf1e = memo(({children, ...rest}) => {
    const on_click_4d89b3c41e66816c6e92dcc4eae84781 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.more_popular", ({ ["kind"] : "series" }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])
const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        jsx("button",{...mergeSlotProps(rest, ({ className:"shelf-more", disabled:reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.busy_rx_state_, onClick:on_click_4d89b3c41e66816c6e92dcc4eae84781, type:"button" }))},children)
    )
});
Button_button_07ddfc544246fcdba2120f7e6da99cc4_3e8caf1e.displayName = "Button";
return Button_button_07ddfc544246fcdba2120f7e6da99cc4_3e8caf1e;
})();

export const Cond_comp_6977ee3e9b538b6377c381443fa91261_3e8caf1e = /*#__PURE__*/ (() => {
const Cond_comp_6977ee3e9b538b6377c381443fa91261_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        (!(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.popular_exhausted_rx_state_.includes("series"))?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_6977ee3e9b538b6377c381443fa91261_3e8caf1e.displayName = "Cond";
return Cond_comp_6977ee3e9b538b6377c381443fa91261_3e8caf1e;
})();

export const Cond_comp_5474f3216aa33ee454650540858ea56d_3e8caf1e = /*#__PURE__*/ (() => {
const Cond_comp_5474f3216aa33ee454650540858ea56d_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        ((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.popular_series_rx_state_.length > 0)?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_5474f3216aa33ee454650540858ea56d_3e8caf1e.displayName = "Cond";
return Cond_comp_5474f3216aa33ee454650540858ea56d_3e8caf1e;
})();

export const Button_button_52896e9dd5132ea8bc5b972179c319b5_3e8caf1e = /*#__PURE__*/ (() => {
const Button_button_52896e9dd5132ea8bc5b972179c319b5_3e8caf1e = memo(({children, ...rest}) => {
    const on_click_5c59fb70583a519d0c56d7779aeba7f7 = useCallback(((_e) => (addEvents([(ReflexEvent("_call_script", ({ ["javascript_code"] : "(() => { const row = document.getElementById('series_rated');\n        if (row) row.scrollBy({left: row.clientWidth * .85 * -1,\n        behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth'}); })()", ["callback"] : null }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])



    return(
        jsx("button",{...mergeSlotProps(rest, ({ "aria-controls":"series_rated", "aria-label":"Anteriores: S\u00e9ries muito bem avaliadas", className:"shelf-arrow", onClick:on_click_5c59fb70583a519d0c56d7779aeba7f7, type:"button" }))},children)
    )
});
Button_button_52896e9dd5132ea8bc5b972179c319b5_3e8caf1e.displayName = "Button";
return Button_button_52896e9dd5132ea8bc5b972179c319b5_3e8caf1e;
})();

export const Button_button_33a2b360f7ce003e1d6f296ab60f8201_3e8caf1e = /*#__PURE__*/ (() => {
const Button_button_33a2b360f7ce003e1d6f296ab60f8201_3e8caf1e = memo(({children, ...rest}) => {
    const on_click_c7054c8a82d6529ce02ef5a794a47d1c = useCallback(((_e) => (addEvents([(ReflexEvent("_call_script", ({ ["javascript_code"] : "(() => { const row = document.getElementById('series_rated');\n        if (row) row.scrollBy({left: row.clientWidth * .85 * 1,\n        behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth'}); })()", ["callback"] : null }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])



    return(
        jsx("button",{...mergeSlotProps(rest, ({ "aria-controls":"series_rated", "aria-label":"Pr\u00f3ximos: S\u00e9ries muito bem avaliadas", className:"shelf-arrow", onClick:on_click_c7054c8a82d6529ce02ef5a794a47d1c, type:"button" }))},children)
    )
});
Button_button_33a2b360f7ce003e1d6f296ab60f8201_3e8caf1e.displayName = "Button";
return Button_button_33a2b360f7ce003e1d6f296ab60f8201_3e8caf1e;
})();

export const Foreach_comp_ceabcacfcb72f0e21ce276dc8c55078c_3e8caf1e = /*#__PURE__*/ (() => {
const Foreach_comp_ceabcacfcb72f0e21ce276dc8c55078c_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        Array.prototype.map.call(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.home_collections_rx_state_?.["series_rated"] ?? [],((m_rx_state_,index_rx_state_)=>(jsx("button",{className:"shelf-card",key:m_rx_state_?.["key"],onClick:((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.open_featured", ({ ["source"] : m_rx_state_?.["source"], ["identifier"] : m_rx_state_?.["external_id"], ["kind"] : "series" }), ({  })))], [_e], ({  })))),type:"button"},jsx("div",{className:"shelf-poster"},jsx("div",{className:"cover-frame"},jsx("div",{"aria-hidden":true,className:"cover-placeholder"},jsx("span",{className:"cover-placeholder-brand"},"CODEBOXD"),jsx("div",{className:"cover-placeholder-copy"},jsx("span",{className:"cover-placeholder-label"},"Capa indispon\u00edvel"))),jsx(Fragment,{},(pyAnd(!((m_rx_state_?.["cover"]?.valueOf?.() === ""?.valueOf?.())), () => (!(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.failed_covers_rx_state_.includes(m_rx_state_?.["cover"]))))?(jsx(Fragment,{},jsx("img",{alt:m_rx_state_?.["title"],className:"media-cover",css:({ ["width"] : "100%", ["height"] : "100%" }),decoding:"async",loading:"lazy",onError:((...args) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.cover_failed", ({ ["url"] : m_rx_state_?.["cover"] }), ({  })))], args, ({  })))),src:m_rx_state_?.["cover"]},))):(jsx(Fragment,{},)))))),jsx("div",{className:"shelf-card-copy"},jsx("h3",{className:"shelf-card-title"},m_rx_state_?.["title"]),jsx("p",{className:"shelf-card-meta"},((m_rx_state_?.["kind"]+" \u00b7 ")+m_rx_state_?.["year"])))))))
    )
});
Foreach_comp_ceabcacfcb72f0e21ce276dc8c55078c_3e8caf1e.displayName = "Foreach";
return Foreach_comp_ceabcacfcb72f0e21ce276dc8c55078c_3e8caf1e;
})();

export const Bare_comp_72ee4fb1e161e0a8b1df0e8ad8491c0e_3e8caf1e = /*#__PURE__*/ (() => {
const Bare_comp_72ee4fb1e161e0a8b1df0e8ad8491c0e_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        (reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.home_collection_errors_rx_state_.includes("series_rated") ? "Esta sele\u00e7\u00e3o est\u00e1 indispon\u00edvel no momento." : "Ainda n\u00e3o h\u00e1 t\u00edtulos nesta sele\u00e7\u00e3o.")
    )
});
Bare_comp_72ee4fb1e161e0a8b1df0e8ad8491c0e_3e8caf1e.displayName = "Bare";
return Bare_comp_72ee4fb1e161e0a8b1df0e8ad8491c0e_3e8caf1e;
})();

export const Cond_comp_cad03517b7a160ddebfe01827bac1ba9_3e8caf1e = /*#__PURE__*/ (() => {
const Cond_comp_cad03517b7a160ddebfe01827bac1ba9_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        ((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.home_collections_rx_state_?.["series_rated"].length > 0)?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_cad03517b7a160ddebfe01827bac1ba9_3e8caf1e.displayName = "Cond";
return Cond_comp_cad03517b7a160ddebfe01827bac1ba9_3e8caf1e;
})();

export const Button_button_75018a6cf27bce127dbdb46661fae973_3e8caf1e = /*#__PURE__*/ (() => {
const Button_button_75018a6cf27bce127dbdb46661fae973_3e8caf1e = memo(({children, ...rest}) => {
    const on_click_0ec79e19b5130cfa25953ca825bbdb1f = useCallback(((_e) => (addEvents([(ReflexEvent("_call_script", ({ ["javascript_code"] : "(() => { const row = document.getElementById('books_popular');\n        if (row) row.scrollBy({left: row.clientWidth * .85 * -1,\n        behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth'}); })()", ["callback"] : null }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])



    return(
        jsx("button",{...mergeSlotProps(rest, ({ "aria-controls":"books_popular", "aria-label":"Anteriores: Livros conhecidos e populares", className:"shelf-arrow", onClick:on_click_0ec79e19b5130cfa25953ca825bbdb1f, type:"button" }))},children)
    )
});
Button_button_75018a6cf27bce127dbdb46661fae973_3e8caf1e.displayName = "Button";
return Button_button_75018a6cf27bce127dbdb46661fae973_3e8caf1e;
})();

export const Button_button_1fc74ee7e121a4bd8251b382ab14cfce_3e8caf1e = /*#__PURE__*/ (() => {
const Button_button_1fc74ee7e121a4bd8251b382ab14cfce_3e8caf1e = memo(({children, ...rest}) => {
    const on_click_56794afdaec6466c99b07b2d74f491e9 = useCallback(((_e) => (addEvents([(ReflexEvent("_call_script", ({ ["javascript_code"] : "(() => { const row = document.getElementById('books_popular');\n        if (row) row.scrollBy({left: row.clientWidth * .85 * 1,\n        behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth'}); })()", ["callback"] : null }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])



    return(
        jsx("button",{...mergeSlotProps(rest, ({ "aria-controls":"books_popular", "aria-label":"Pr\u00f3ximos: Livros conhecidos e populares", className:"shelf-arrow", onClick:on_click_56794afdaec6466c99b07b2d74f491e9, type:"button" }))},children)
    )
});
Button_button_1fc74ee7e121a4bd8251b382ab14cfce_3e8caf1e.displayName = "Button";
return Button_button_1fc74ee7e121a4bd8251b382ab14cfce_3e8caf1e;
})();

export const Foreach_comp_0cb0f1f5e0d84a726ec178b0d5b7f1c9_3e8caf1e = /*#__PURE__*/ (() => {
const Foreach_comp_0cb0f1f5e0d84a726ec178b0d5b7f1c9_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        Array.prototype.map.call(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.home_collections_rx_state_?.["books_popular"] ?? [],((m_rx_state_,index_rx_state_)=>(jsx("button",{className:"shelf-card",key:m_rx_state_?.["key"],onClick:((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.open_featured", ({ ["source"] : m_rx_state_?.["source"], ["identifier"] : m_rx_state_?.["external_id"], ["kind"] : "book" }), ({  })))], [_e], ({  })))),type:"button"},jsx("div",{className:"shelf-poster"},jsx("div",{className:"cover-frame"},jsx("div",{"aria-hidden":true,className:"cover-placeholder"},jsx("span",{className:"cover-placeholder-brand"},"CODEBOXD"),jsx("div",{className:"cover-placeholder-copy"},jsx("span",{className:"cover-placeholder-label"},"Capa indispon\u00edvel"))),jsx(Fragment,{},(pyAnd(!((m_rx_state_?.["cover"]?.valueOf?.() === ""?.valueOf?.())), () => (!(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.failed_covers_rx_state_.includes(m_rx_state_?.["cover"]))))?(jsx(Fragment,{},jsx("img",{alt:m_rx_state_?.["title"],className:"media-cover",css:({ ["width"] : "100%", ["height"] : "100%" }),decoding:"async",loading:"lazy",onError:((...args) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.cover_failed", ({ ["url"] : m_rx_state_?.["cover"] }), ({  })))], args, ({  })))),src:m_rx_state_?.["cover"]},))):(jsx(Fragment,{},)))))),jsx("div",{className:"shelf-card-copy"},jsx("h3",{className:"shelf-card-title"},m_rx_state_?.["title"]),jsx("p",{className:"shelf-card-meta"},((m_rx_state_?.["kind"]+" \u00b7 ")+m_rx_state_?.["year"])))))))
    )
});
Foreach_comp_0cb0f1f5e0d84a726ec178b0d5b7f1c9_3e8caf1e.displayName = "Foreach";
return Foreach_comp_0cb0f1f5e0d84a726ec178b0d5b7f1c9_3e8caf1e;
})();

export const Bare_comp_b8ad0d41121cd47fc55cf8708645673f_3e8caf1e = /*#__PURE__*/ (() => {
const Bare_comp_b8ad0d41121cd47fc55cf8708645673f_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        (reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.home_collection_errors_rx_state_.includes("books_popular") ? "Esta sele\u00e7\u00e3o est\u00e1 indispon\u00edvel no momento." : "Ainda n\u00e3o h\u00e1 t\u00edtulos nesta sele\u00e7\u00e3o.")
    )
});
Bare_comp_b8ad0d41121cd47fc55cf8708645673f_3e8caf1e.displayName = "Bare";
return Bare_comp_b8ad0d41121cd47fc55cf8708645673f_3e8caf1e;
})();

export const Cond_comp_4e12166b6f96141ac8e5ab5b4a70082a_3e8caf1e = /*#__PURE__*/ (() => {
const Cond_comp_4e12166b6f96141ac8e5ab5b4a70082a_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        ((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.home_collections_rx_state_?.["books_popular"].length > 0)?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_4e12166b6f96141ac8e5ab5b4a70082a_3e8caf1e.displayName = "Cond";
return Cond_comp_4e12166b6f96141ac8e5ab5b4a70082a_3e8caf1e;
})();

export const Button_button_9f89e00f826ccbc42763a3dbc7b7916d_3e8caf1e = /*#__PURE__*/ (() => {
const Button_button_9f89e00f826ccbc42763a3dbc7b7916d_3e8caf1e = memo(({children, ...rest}) => {
    const on_click_8c5d619e65a1b008e029972b3ca028e1 = useCallback(((_e) => (addEvents([(ReflexEvent("_call_script", ({ ["javascript_code"] : "(() => { const row = document.getElementById('books_fiction');\n        if (row) row.scrollBy({left: row.clientWidth * .85 * -1,\n        behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth'}); })()", ["callback"] : null }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])



    return(
        jsx("button",{...mergeSlotProps(rest, ({ "aria-controls":"books_fiction", "aria-label":"Anteriores: Sua pr\u00f3xima leitura", className:"shelf-arrow", onClick:on_click_8c5d619e65a1b008e029972b3ca028e1, type:"button" }))},children)
    )
});
Button_button_9f89e00f826ccbc42763a3dbc7b7916d_3e8caf1e.displayName = "Button";
return Button_button_9f89e00f826ccbc42763a3dbc7b7916d_3e8caf1e;
})();

export const Button_button_88598ff3809f47039b07e7168f50dfe0_3e8caf1e = /*#__PURE__*/ (() => {
const Button_button_88598ff3809f47039b07e7168f50dfe0_3e8caf1e = memo(({children, ...rest}) => {
    const on_click_11be31653bdeef507e9e1815f113624d = useCallback(((_e) => (addEvents([(ReflexEvent("_call_script", ({ ["javascript_code"] : "(() => { const row = document.getElementById('books_fiction');\n        if (row) row.scrollBy({left: row.clientWidth * .85 * 1,\n        behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth'}); })()", ["callback"] : null }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])



    return(
        jsx("button",{...mergeSlotProps(rest, ({ "aria-controls":"books_fiction", "aria-label":"Pr\u00f3ximos: Sua pr\u00f3xima leitura", className:"shelf-arrow", onClick:on_click_11be31653bdeef507e9e1815f113624d, type:"button" }))},children)
    )
});
Button_button_88598ff3809f47039b07e7168f50dfe0_3e8caf1e.displayName = "Button";
return Button_button_88598ff3809f47039b07e7168f50dfe0_3e8caf1e;
})();

export const Foreach_comp_ce5ea81743541d03f9cf2013451428c7_3e8caf1e = /*#__PURE__*/ (() => {
const Foreach_comp_ce5ea81743541d03f9cf2013451428c7_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        Array.prototype.map.call(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.home_collections_rx_state_?.["books_fiction"] ?? [],((m_rx_state_,index_rx_state_)=>(jsx("button",{className:"shelf-card",key:m_rx_state_?.["key"],onClick:((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.open_featured", ({ ["source"] : m_rx_state_?.["source"], ["identifier"] : m_rx_state_?.["external_id"], ["kind"] : "book" }), ({  })))], [_e], ({  })))),type:"button"},jsx("div",{className:"shelf-poster"},jsx("div",{className:"cover-frame"},jsx("div",{"aria-hidden":true,className:"cover-placeholder"},jsx("span",{className:"cover-placeholder-brand"},"CODEBOXD"),jsx("div",{className:"cover-placeholder-copy"},jsx("span",{className:"cover-placeholder-label"},"Capa indispon\u00edvel"))),jsx(Fragment,{},(pyAnd(!((m_rx_state_?.["cover"]?.valueOf?.() === ""?.valueOf?.())), () => (!(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.failed_covers_rx_state_.includes(m_rx_state_?.["cover"]))))?(jsx(Fragment,{},jsx("img",{alt:m_rx_state_?.["title"],className:"media-cover",css:({ ["width"] : "100%", ["height"] : "100%" }),decoding:"async",loading:"lazy",onError:((...args) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.cover_failed", ({ ["url"] : m_rx_state_?.["cover"] }), ({  })))], args, ({  })))),src:m_rx_state_?.["cover"]},))):(jsx(Fragment,{},)))))),jsx("div",{className:"shelf-card-copy"},jsx("h3",{className:"shelf-card-title"},m_rx_state_?.["title"]),jsx("p",{className:"shelf-card-meta"},((m_rx_state_?.["kind"]+" \u00b7 ")+m_rx_state_?.["year"])))))))
    )
});
Foreach_comp_ce5ea81743541d03f9cf2013451428c7_3e8caf1e.displayName = "Foreach";
return Foreach_comp_ce5ea81743541d03f9cf2013451428c7_3e8caf1e;
})();

export const Bare_comp_2e17366f23fc9a6489ced832874a03a8_3e8caf1e = /*#__PURE__*/ (() => {
const Bare_comp_2e17366f23fc9a6489ced832874a03a8_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        (reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.home_collection_errors_rx_state_.includes("books_fiction") ? "Esta sele\u00e7\u00e3o est\u00e1 indispon\u00edvel no momento." : "Ainda n\u00e3o h\u00e1 t\u00edtulos nesta sele\u00e7\u00e3o.")
    )
});
Bare_comp_2e17366f23fc9a6489ced832874a03a8_3e8caf1e.displayName = "Bare";
return Bare_comp_2e17366f23fc9a6489ced832874a03a8_3e8caf1e;
})();

export const Cond_comp_91dfcbc00205990a77dad4ff23650a24_3e8caf1e = /*#__PURE__*/ (() => {
const Cond_comp_91dfcbc00205990a77dad4ff23650a24_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        ((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.home_collections_rx_state_?.["books_fiction"].length > 0)?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_91dfcbc00205990a77dad4ff23650a24_3e8caf1e.displayName = "Cond";
return Cond_comp_91dfcbc00205990a77dad4ff23650a24_3e8caf1e;
})();

export const Button_button_d99b06cc7029cd31499074f91d45b1f8_3e8caf1e = /*#__PURE__*/ (() => {
const Button_button_d99b06cc7029cd31499074f91d45b1f8_3e8caf1e = memo(({children, ...rest}) => {
    const on_click_bef57cea62557b7ac19827f1e600cdad = useCallback(((_e) => (addEvents([(ReflexEvent("_call_script", ({ ["javascript_code"] : "(() => { const row = document.getElementById('books_fantasy');\n        if (row) row.scrollBy({left: row.clientWidth * .85 * -1,\n        behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth'}); })()", ["callback"] : null }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])



    return(
        jsx("button",{...mergeSlotProps(rest, ({ "aria-controls":"books_fantasy", "aria-label":"Anteriores: Livros de fantasia", className:"shelf-arrow", onClick:on_click_bef57cea62557b7ac19827f1e600cdad, type:"button" }))},children)
    )
});
Button_button_d99b06cc7029cd31499074f91d45b1f8_3e8caf1e.displayName = "Button";
return Button_button_d99b06cc7029cd31499074f91d45b1f8_3e8caf1e;
})();

export const Button_button_59478a377d67b6fa7cf0b22eeab51913_3e8caf1e = /*#__PURE__*/ (() => {
const Button_button_59478a377d67b6fa7cf0b22eeab51913_3e8caf1e = memo(({children, ...rest}) => {
    const on_click_1c75a86c60be5a2bc278cea89a7553c6 = useCallback(((_e) => (addEvents([(ReflexEvent("_call_script", ({ ["javascript_code"] : "(() => { const row = document.getElementById('books_fantasy');\n        if (row) row.scrollBy({left: row.clientWidth * .85 * 1,\n        behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth'}); })()", ["callback"] : null }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])



    return(
        jsx("button",{...mergeSlotProps(rest, ({ "aria-controls":"books_fantasy", "aria-label":"Pr\u00f3ximos: Livros de fantasia", className:"shelf-arrow", onClick:on_click_1c75a86c60be5a2bc278cea89a7553c6, type:"button" }))},children)
    )
});
Button_button_59478a377d67b6fa7cf0b22eeab51913_3e8caf1e.displayName = "Button";
return Button_button_59478a377d67b6fa7cf0b22eeab51913_3e8caf1e;
})();

export const Foreach_comp_6198122503e7272f7eef227add745fe3_3e8caf1e = /*#__PURE__*/ (() => {
const Foreach_comp_6198122503e7272f7eef227add745fe3_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        Array.prototype.map.call(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.home_collections_rx_state_?.["books_fantasy"] ?? [],((m_rx_state_,index_rx_state_)=>(jsx("button",{className:"shelf-card",key:m_rx_state_?.["key"],onClick:((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.open_featured", ({ ["source"] : m_rx_state_?.["source"], ["identifier"] : m_rx_state_?.["external_id"], ["kind"] : "book" }), ({  })))], [_e], ({  })))),type:"button"},jsx("div",{className:"shelf-poster"},jsx("div",{className:"cover-frame"},jsx("div",{"aria-hidden":true,className:"cover-placeholder"},jsx("span",{className:"cover-placeholder-brand"},"CODEBOXD"),jsx("div",{className:"cover-placeholder-copy"},jsx("span",{className:"cover-placeholder-label"},"Capa indispon\u00edvel"))),jsx(Fragment,{},(pyAnd(!((m_rx_state_?.["cover"]?.valueOf?.() === ""?.valueOf?.())), () => (!(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.failed_covers_rx_state_.includes(m_rx_state_?.["cover"]))))?(jsx(Fragment,{},jsx("img",{alt:m_rx_state_?.["title"],className:"media-cover",css:({ ["width"] : "100%", ["height"] : "100%" }),decoding:"async",loading:"lazy",onError:((...args) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.cover_failed", ({ ["url"] : m_rx_state_?.["cover"] }), ({  })))], args, ({  })))),src:m_rx_state_?.["cover"]},))):(jsx(Fragment,{},)))))),jsx("div",{className:"shelf-card-copy"},jsx("h3",{className:"shelf-card-title"},m_rx_state_?.["title"]),jsx("p",{className:"shelf-card-meta"},((m_rx_state_?.["kind"]+" \u00b7 ")+m_rx_state_?.["year"])))))))
    )
});
Foreach_comp_6198122503e7272f7eef227add745fe3_3e8caf1e.displayName = "Foreach";
return Foreach_comp_6198122503e7272f7eef227add745fe3_3e8caf1e;
})();

export const Bare_comp_5f014aa285c679d4347f87cd4aa42296_3e8caf1e = /*#__PURE__*/ (() => {
const Bare_comp_5f014aa285c679d4347f87cd4aa42296_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        (reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.home_collection_errors_rx_state_.includes("books_fantasy") ? "Esta sele\u00e7\u00e3o est\u00e1 indispon\u00edvel no momento." : "Ainda n\u00e3o h\u00e1 t\u00edtulos nesta sele\u00e7\u00e3o.")
    )
});
Bare_comp_5f014aa285c679d4347f87cd4aa42296_3e8caf1e.displayName = "Bare";
return Bare_comp_5f014aa285c679d4347f87cd4aa42296_3e8caf1e;
})();

export const Cond_comp_799de69b856cf26ac8d7ec50b839bbd4_3e8caf1e = /*#__PURE__*/ (() => {
const Cond_comp_799de69b856cf26ac8d7ec50b839bbd4_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        ((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.home_collections_rx_state_?.["books_fantasy"].length > 0)?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_799de69b856cf26ac8d7ec50b839bbd4_3e8caf1e.displayName = "Cond";
return Cond_comp_799de69b856cf26ac8d7ec50b839bbd4_3e8caf1e;
})();

export const Button_button_f4ef24a37b887162c8e648748cb55e9d_3e8caf1e = /*#__PURE__*/ (() => {
const Button_button_f4ef24a37b887162c8e648748cb55e9d_3e8caf1e = memo(({children, ...rest}) => {
    const on_click_b637042974079ee8be994c277e2d8172 = useCallback(((_e) => (addEvents([(ReflexEvent("_call_script", ({ ["javascript_code"] : "(() => { const row = document.getElementById('books_mystery');\n        if (row) row.scrollBy({left: row.clientWidth * .85 * -1,\n        behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth'}); })()", ["callback"] : null }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])



    return(
        jsx("button",{...mergeSlotProps(rest, ({ "aria-controls":"books_mystery", "aria-label":"Anteriores: Mist\u00e9rios entre p\u00e1ginas", className:"shelf-arrow", onClick:on_click_b637042974079ee8be994c277e2d8172, type:"button" }))},children)
    )
});
Button_button_f4ef24a37b887162c8e648748cb55e9d_3e8caf1e.displayName = "Button";
return Button_button_f4ef24a37b887162c8e648748cb55e9d_3e8caf1e;
})();

export const Button_button_caf0009c3fe50b80bec5e79bc29edf20_3e8caf1e = /*#__PURE__*/ (() => {
const Button_button_caf0009c3fe50b80bec5e79bc29edf20_3e8caf1e = memo(({children, ...rest}) => {
    const on_click_7c3055fad0d8401201eec2989bc9e31e = useCallback(((_e) => (addEvents([(ReflexEvent("_call_script", ({ ["javascript_code"] : "(() => { const row = document.getElementById('books_mystery');\n        if (row) row.scrollBy({left: row.clientWidth * .85 * 1,\n        behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth'}); })()", ["callback"] : null }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])



    return(
        jsx("button",{...mergeSlotProps(rest, ({ "aria-controls":"books_mystery", "aria-label":"Pr\u00f3ximos: Mist\u00e9rios entre p\u00e1ginas", className:"shelf-arrow", onClick:on_click_7c3055fad0d8401201eec2989bc9e31e, type:"button" }))},children)
    )
});
Button_button_caf0009c3fe50b80bec5e79bc29edf20_3e8caf1e.displayName = "Button";
return Button_button_caf0009c3fe50b80bec5e79bc29edf20_3e8caf1e;
})();

export const Foreach_comp_b0b95c8dd3fea8d349296f980b30219f_3e8caf1e = /*#__PURE__*/ (() => {
const Foreach_comp_b0b95c8dd3fea8d349296f980b30219f_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        Array.prototype.map.call(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.home_collections_rx_state_?.["books_mystery"] ?? [],((m_rx_state_,index_rx_state_)=>(jsx("button",{className:"shelf-card",key:m_rx_state_?.["key"],onClick:((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.open_featured", ({ ["source"] : m_rx_state_?.["source"], ["identifier"] : m_rx_state_?.["external_id"], ["kind"] : "book" }), ({  })))], [_e], ({  })))),type:"button"},jsx("div",{className:"shelf-poster"},jsx("div",{className:"cover-frame"},jsx("div",{"aria-hidden":true,className:"cover-placeholder"},jsx("span",{className:"cover-placeholder-brand"},"CODEBOXD"),jsx("div",{className:"cover-placeholder-copy"},jsx("span",{className:"cover-placeholder-label"},"Capa indispon\u00edvel"))),jsx(Fragment,{},(pyAnd(!((m_rx_state_?.["cover"]?.valueOf?.() === ""?.valueOf?.())), () => (!(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.failed_covers_rx_state_.includes(m_rx_state_?.["cover"]))))?(jsx(Fragment,{},jsx("img",{alt:m_rx_state_?.["title"],className:"media-cover",css:({ ["width"] : "100%", ["height"] : "100%" }),decoding:"async",loading:"lazy",onError:((...args) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.cover_failed", ({ ["url"] : m_rx_state_?.["cover"] }), ({  })))], args, ({  })))),src:m_rx_state_?.["cover"]},))):(jsx(Fragment,{},)))))),jsx("div",{className:"shelf-card-copy"},jsx("h3",{className:"shelf-card-title"},m_rx_state_?.["title"]),jsx("p",{className:"shelf-card-meta"},((m_rx_state_?.["kind"]+" \u00b7 ")+m_rx_state_?.["year"])))))))
    )
});
Foreach_comp_b0b95c8dd3fea8d349296f980b30219f_3e8caf1e.displayName = "Foreach";
return Foreach_comp_b0b95c8dd3fea8d349296f980b30219f_3e8caf1e;
})();

export const Bare_comp_a87822c4f8ba2a357130f1dfa99f3230_3e8caf1e = /*#__PURE__*/ (() => {
const Bare_comp_a87822c4f8ba2a357130f1dfa99f3230_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        (reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.home_collection_errors_rx_state_.includes("books_mystery") ? "Esta sele\u00e7\u00e3o est\u00e1 indispon\u00edvel no momento." : "Ainda n\u00e3o h\u00e1 t\u00edtulos nesta sele\u00e7\u00e3o.")
    )
});
Bare_comp_a87822c4f8ba2a357130f1dfa99f3230_3e8caf1e.displayName = "Bare";
return Bare_comp_a87822c4f8ba2a357130f1dfa99f3230_3e8caf1e;
})();

export const Cond_comp_b689266125384d143102921dbba94db1_3e8caf1e = /*#__PURE__*/ (() => {
const Cond_comp_b689266125384d143102921dbba94db1_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        ((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.home_collections_rx_state_?.["books_mystery"].length > 0)?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_b689266125384d143102921dbba94db1_3e8caf1e.displayName = "Cond";
return Cond_comp_b689266125384d143102921dbba94db1_3e8caf1e;
})();

export const Button_button_eee312becabe6f173ccc3076b2e4738e_3e8caf1e = /*#__PURE__*/ (() => {
const Button_button_eee312becabe6f173ccc3076b2e4738e_3e8caf1e = memo(({children, ...rest}) => {
    const on_click_e133b6990ce1cc42a34ae6a7e82615f3 = useCallback(((_e) => (addEvents([(ReflexEvent("_call_script", ({ ["javascript_code"] : "(() => { const row = document.getElementById('books_game_theory');\n        if (row) row.scrollBy({left: row.clientWidth * .85 * -1,\n        behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth'}); })()", ["callback"] : null }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])



    return(
        jsx("button",{...mergeSlotProps(rest, ({ "aria-controls":"books_game_theory", "aria-label":"Anteriores: Teoria dos Jogos", className:"shelf-arrow", onClick:on_click_e133b6990ce1cc42a34ae6a7e82615f3, type:"button" }))},children)
    )
});
Button_button_eee312becabe6f173ccc3076b2e4738e_3e8caf1e.displayName = "Button";
return Button_button_eee312becabe6f173ccc3076b2e4738e_3e8caf1e;
})();

export const Button_button_44c333386c02dce9e6ccc2d57cf00040_3e8caf1e = /*#__PURE__*/ (() => {
const Button_button_44c333386c02dce9e6ccc2d57cf00040_3e8caf1e = memo(({children, ...rest}) => {
    const on_click_17a8e790b3ba6c343c7b353f208ffbd5 = useCallback(((_e) => (addEvents([(ReflexEvent("_call_script", ({ ["javascript_code"] : "(() => { const row = document.getElementById('books_game_theory');\n        if (row) row.scrollBy({left: row.clientWidth * .85 * 1,\n        behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth'}); })()", ["callback"] : null }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])



    return(
        jsx("button",{...mergeSlotProps(rest, ({ "aria-controls":"books_game_theory", "aria-label":"Pr\u00f3ximos: Teoria dos Jogos", className:"shelf-arrow", onClick:on_click_17a8e790b3ba6c343c7b353f208ffbd5, type:"button" }))},children)
    )
});
Button_button_44c333386c02dce9e6ccc2d57cf00040_3e8caf1e.displayName = "Button";
return Button_button_44c333386c02dce9e6ccc2d57cf00040_3e8caf1e;
})();

export const Foreach_comp_8e55cacdf14761b4b015072b9d2e5e1d_3e8caf1e = /*#__PURE__*/ (() => {
const Foreach_comp_8e55cacdf14761b4b015072b9d2e5e1d_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        Array.prototype.map.call(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.home_collections_rx_state_?.["books_game_theory"] ?? [],((m_rx_state_,index_rx_state_)=>(jsx("button",{className:"shelf-card",key:m_rx_state_?.["key"],onClick:((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.open_featured", ({ ["source"] : m_rx_state_?.["source"], ["identifier"] : m_rx_state_?.["external_id"], ["kind"] : "book" }), ({  })))], [_e], ({  })))),type:"button"},jsx("div",{className:"shelf-poster"},jsx("div",{className:"cover-frame"},jsx("div",{"aria-hidden":true,className:"cover-placeholder"},jsx("span",{className:"cover-placeholder-brand"},"CODEBOXD"),jsx("div",{className:"cover-placeholder-copy"},jsx("span",{className:"cover-placeholder-label"},"Capa indispon\u00edvel"))),jsx(Fragment,{},(pyAnd(!((m_rx_state_?.["cover"]?.valueOf?.() === ""?.valueOf?.())), () => (!(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.failed_covers_rx_state_.includes(m_rx_state_?.["cover"]))))?(jsx(Fragment,{},jsx("img",{alt:m_rx_state_?.["title"],className:"media-cover",css:({ ["width"] : "100%", ["height"] : "100%" }),decoding:"async",loading:"lazy",onError:((...args) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.cover_failed", ({ ["url"] : m_rx_state_?.["cover"] }), ({  })))], args, ({  })))),src:m_rx_state_?.["cover"]},))):(jsx(Fragment,{},)))))),jsx("div",{className:"shelf-card-copy"},jsx("h3",{className:"shelf-card-title"},m_rx_state_?.["title"]),jsx("p",{className:"shelf-card-meta"},((m_rx_state_?.["kind"]+" \u00b7 ")+m_rx_state_?.["year"])))))))
    )
});
Foreach_comp_8e55cacdf14761b4b015072b9d2e5e1d_3e8caf1e.displayName = "Foreach";
return Foreach_comp_8e55cacdf14761b4b015072b9d2e5e1d_3e8caf1e;
})();

export const Bare_comp_c595067e0349293fe5ab1c6ed8ddb197_3e8caf1e = /*#__PURE__*/ (() => {
const Bare_comp_c595067e0349293fe5ab1c6ed8ddb197_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        (reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.home_collection_errors_rx_state_.includes("books_game_theory") ? "Esta sele\u00e7\u00e3o est\u00e1 indispon\u00edvel no momento." : "Ainda n\u00e3o h\u00e1 t\u00edtulos nesta sele\u00e7\u00e3o.")
    )
});
Bare_comp_c595067e0349293fe5ab1c6ed8ddb197_3e8caf1e.displayName = "Bare";
return Bare_comp_c595067e0349293fe5ab1c6ed8ddb197_3e8caf1e;
})();

export const Cond_comp_9cd1b158155cd86efad7678d7984eae9_3e8caf1e = /*#__PURE__*/ (() => {
const Cond_comp_9cd1b158155cd86efad7678d7984eae9_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        ((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.home_collections_rx_state_?.["books_game_theory"].length > 0)?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_9cd1b158155cd86efad7678d7984eae9_3e8caf1e.displayName = "Cond";
return Cond_comp_9cd1b158155cd86efad7678d7984eae9_3e8caf1e;
})();

export const Button_button_2fdeef6dc24a3033a75524a95343d82c_3e8caf1e = /*#__PURE__*/ (() => {
const Button_button_2fdeef6dc24a3033a75524a95343d82c_3e8caf1e = memo(({children, ...rest}) => {
    const on_click_c71ddc52e9b56886fa751f4199149833 = useCallback(((_e) => (addEvents([(ReflexEvent("_call_script", ({ ["javascript_code"] : "(() => { const row = document.getElementById('anime_rated');\n        if (row) row.scrollBy({left: row.clientWidth * .85 * -1,\n        behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth'}); })()", ["callback"] : null }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])



    return(
        jsx("button",{...mergeSlotProps(rest, ({ "aria-controls":"anime_rated", "aria-label":"Anteriores: Animes muito bem avaliados", className:"shelf-arrow", onClick:on_click_c71ddc52e9b56886fa751f4199149833, type:"button" }))},children)
    )
});
Button_button_2fdeef6dc24a3033a75524a95343d82c_3e8caf1e.displayName = "Button";
return Button_button_2fdeef6dc24a3033a75524a95343d82c_3e8caf1e;
})();

export const Button_button_37e00598b294aae7dc2d0721c595d034_3e8caf1e = /*#__PURE__*/ (() => {
const Button_button_37e00598b294aae7dc2d0721c595d034_3e8caf1e = memo(({children, ...rest}) => {
    const on_click_297747bf7786e60c304128a8c3bbe622 = useCallback(((_e) => (addEvents([(ReflexEvent("_call_script", ({ ["javascript_code"] : "(() => { const row = document.getElementById('anime_rated');\n        if (row) row.scrollBy({left: row.clientWidth * .85 * 1,\n        behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth'}); })()", ["callback"] : null }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])



    return(
        jsx("button",{...mergeSlotProps(rest, ({ "aria-controls":"anime_rated", "aria-label":"Pr\u00f3ximos: Animes muito bem avaliados", className:"shelf-arrow", onClick:on_click_297747bf7786e60c304128a8c3bbe622, type:"button" }))},children)
    )
});
Button_button_37e00598b294aae7dc2d0721c595d034_3e8caf1e.displayName = "Button";
return Button_button_37e00598b294aae7dc2d0721c595d034_3e8caf1e;
})();

export const Foreach_comp_a4ecdc9afa834687fa7ffb50f9d4f601_3e8caf1e = /*#__PURE__*/ (() => {
const Foreach_comp_a4ecdc9afa834687fa7ffb50f9d4f601_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        Array.prototype.map.call(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.home_collections_rx_state_?.["anime_rated"] ?? [],((m_rx_state_,index_rx_state_)=>(jsx("button",{className:"shelf-card",key:m_rx_state_?.["key"],onClick:((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.open_featured", ({ ["source"] : m_rx_state_?.["source"], ["identifier"] : m_rx_state_?.["external_id"], ["kind"] : "anime" }), ({  })))], [_e], ({  })))),type:"button"},jsx("div",{className:"shelf-poster"},jsx("div",{className:"cover-frame"},jsx("div",{"aria-hidden":true,className:"cover-placeholder"},jsx("span",{className:"cover-placeholder-brand"},"CODEBOXD"),jsx("div",{className:"cover-placeholder-copy"},jsx("span",{className:"cover-placeholder-label"},"Capa indispon\u00edvel"))),jsx(Fragment,{},(pyAnd(!((m_rx_state_?.["cover"]?.valueOf?.() === ""?.valueOf?.())), () => (!(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.failed_covers_rx_state_.includes(m_rx_state_?.["cover"]))))?(jsx(Fragment,{},jsx("img",{alt:m_rx_state_?.["title"],className:"media-cover",css:({ ["width"] : "100%", ["height"] : "100%" }),decoding:"async",loading:"lazy",onError:((...args) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.cover_failed", ({ ["url"] : m_rx_state_?.["cover"] }), ({  })))], args, ({  })))),src:m_rx_state_?.["cover"]},))):(jsx(Fragment,{},)))))),jsx("div",{className:"shelf-card-copy"},jsx("h3",{className:"shelf-card-title"},m_rx_state_?.["title"]),jsx("p",{className:"shelf-card-meta"},((m_rx_state_?.["kind"]+" \u00b7 ")+m_rx_state_?.["year"])))))))
    )
});
Foreach_comp_a4ecdc9afa834687fa7ffb50f9d4f601_3e8caf1e.displayName = "Foreach";
return Foreach_comp_a4ecdc9afa834687fa7ffb50f9d4f601_3e8caf1e;
})();

export const Bare_comp_5f9979f9bff89ce23c85e35d85bb34b2_3e8caf1e = /*#__PURE__*/ (() => {
const Bare_comp_5f9979f9bff89ce23c85e35d85bb34b2_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        (reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.home_collection_errors_rx_state_.includes("anime_rated") ? "Esta sele\u00e7\u00e3o est\u00e1 indispon\u00edvel no momento." : "Ainda n\u00e3o h\u00e1 t\u00edtulos nesta sele\u00e7\u00e3o.")
    )
});
Bare_comp_5f9979f9bff89ce23c85e35d85bb34b2_3e8caf1e.displayName = "Bare";
return Bare_comp_5f9979f9bff89ce23c85e35d85bb34b2_3e8caf1e;
})();

export const Cond_comp_3030a0a7f6da535ae59a7d1245a13131_3e8caf1e = /*#__PURE__*/ (() => {
const Cond_comp_3030a0a7f6da535ae59a7d1245a13131_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        ((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.home_collections_rx_state_?.["anime_rated"].length > 0)?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_3030a0a7f6da535ae59a7d1245a13131_3e8caf1e.displayName = "Cond";
return Cond_comp_3030a0a7f6da535ae59a7d1245a13131_3e8caf1e;
})();

export const Button_button_690bc5ef7690ebc3349243579e2e9dde_3e8caf1e = /*#__PURE__*/ (() => {
const Button_button_690bc5ef7690ebc3349243579e2e9dde_3e8caf1e = memo(({children, ...rest}) => {
    const on_click_1beb5c297986f619351dda53c9b734f4 = useCallback(((_e) => (addEvents([(ReflexEvent("_call_script", ({ ["javascript_code"] : "(() => { const row = document.getElementById('anime_popular');\n        if (row) row.scrollBy({left: row.clientWidth * .85 * -1,\n        behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth'}); })()", ["callback"] : null }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])



    return(
        jsx("button",{...mergeSlotProps(rest, ({ "aria-controls":"anime_popular", "aria-label":"Anteriores: Animes populares", className:"shelf-arrow", onClick:on_click_1beb5c297986f619351dda53c9b734f4, type:"button" }))},children)
    )
});
Button_button_690bc5ef7690ebc3349243579e2e9dde_3e8caf1e.displayName = "Button";
return Button_button_690bc5ef7690ebc3349243579e2e9dde_3e8caf1e;
})();

export const Button_button_89d59e1d70a2d480ce4f33c6865404db_3e8caf1e = /*#__PURE__*/ (() => {
const Button_button_89d59e1d70a2d480ce4f33c6865404db_3e8caf1e = memo(({children, ...rest}) => {
    const on_click_6638f0ee70f06e608337eb19a6a8bb8e = useCallback(((_e) => (addEvents([(ReflexEvent("_call_script", ({ ["javascript_code"] : "(() => { const row = document.getElementById('anime_popular');\n        if (row) row.scrollBy({left: row.clientWidth * .85 * 1,\n        behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth'}); })()", ["callback"] : null }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])



    return(
        jsx("button",{...mergeSlotProps(rest, ({ "aria-controls":"anime_popular", "aria-label":"Pr\u00f3ximos: Animes populares", className:"shelf-arrow", onClick:on_click_6638f0ee70f06e608337eb19a6a8bb8e, type:"button" }))},children)
    )
});
Button_button_89d59e1d70a2d480ce4f33c6865404db_3e8caf1e.displayName = "Button";
return Button_button_89d59e1d70a2d480ce4f33c6865404db_3e8caf1e;
})();

export const Foreach_comp_652c28c709c988f72ea44bf960e4d4d6_3e8caf1e = /*#__PURE__*/ (() => {
const Foreach_comp_652c28c709c988f72ea44bf960e4d4d6_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        Array.prototype.map.call(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.home_collections_rx_state_?.["anime_popular"] ?? [],((m_rx_state_,index_rx_state_)=>(jsx("button",{className:"shelf-card",key:m_rx_state_?.["key"],onClick:((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.open_featured", ({ ["source"] : m_rx_state_?.["source"], ["identifier"] : m_rx_state_?.["external_id"], ["kind"] : "anime" }), ({  })))], [_e], ({  })))),type:"button"},jsx("div",{className:"shelf-poster"},jsx("div",{className:"cover-frame"},jsx("div",{"aria-hidden":true,className:"cover-placeholder"},jsx("span",{className:"cover-placeholder-brand"},"CODEBOXD"),jsx("div",{className:"cover-placeholder-copy"},jsx("span",{className:"cover-placeholder-label"},"Capa indispon\u00edvel"))),jsx(Fragment,{},(pyAnd(!((m_rx_state_?.["cover"]?.valueOf?.() === ""?.valueOf?.())), () => (!(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.failed_covers_rx_state_.includes(m_rx_state_?.["cover"]))))?(jsx(Fragment,{},jsx("img",{alt:m_rx_state_?.["title"],className:"media-cover",css:({ ["width"] : "100%", ["height"] : "100%" }),decoding:"async",loading:"lazy",onError:((...args) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.cover_failed", ({ ["url"] : m_rx_state_?.["cover"] }), ({  })))], args, ({  })))),src:m_rx_state_?.["cover"]},))):(jsx(Fragment,{},)))))),jsx("div",{className:"shelf-card-copy"},jsx("h3",{className:"shelf-card-title"},m_rx_state_?.["title"]),jsx("p",{className:"shelf-card-meta"},((m_rx_state_?.["kind"]+" \u00b7 ")+m_rx_state_?.["year"])))))))
    )
});
Foreach_comp_652c28c709c988f72ea44bf960e4d4d6_3e8caf1e.displayName = "Foreach";
return Foreach_comp_652c28c709c988f72ea44bf960e4d4d6_3e8caf1e;
})();

export const Bare_comp_80921d373ba9b178abfab0a4e491e41f_3e8caf1e = /*#__PURE__*/ (() => {
const Bare_comp_80921d373ba9b178abfab0a4e491e41f_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        (reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.home_collection_errors_rx_state_.includes("anime_popular") ? "Esta sele\u00e7\u00e3o est\u00e1 indispon\u00edvel no momento." : "Ainda n\u00e3o h\u00e1 t\u00edtulos nesta sele\u00e7\u00e3o.")
    )
});
Bare_comp_80921d373ba9b178abfab0a4e491e41f_3e8caf1e.displayName = "Bare";
return Bare_comp_80921d373ba9b178abfab0a4e491e41f_3e8caf1e;
})();

export const Cond_comp_2f180cdc097012bb0655a59bc0460af6_3e8caf1e = /*#__PURE__*/ (() => {
const Cond_comp_2f180cdc097012bb0655a59bc0460af6_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        ((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.home_collections_rx_state_?.["anime_popular"].length > 0)?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_2f180cdc097012bb0655a59bc0460af6_3e8caf1e.displayName = "Cond";
return Cond_comp_2f180cdc097012bb0655a59bc0460af6_3e8caf1e;
})();

export const Button_button_2dc342d8e8986766ba5cbe91d652a2a9_3e8caf1e = /*#__PURE__*/ (() => {
const Button_button_2dc342d8e8986766ba5cbe91d652a2a9_3e8caf1e = memo(({children, ...rest}) => {
    const on_click_64b7b773124fbc6f016a96db7b9acc40 = useCallback(((_e) => (addEvents([(ReflexEvent("_call_script", ({ ["javascript_code"] : "(() => { const row = document.getElementById('anime_current');\n        if (row) row.scrollBy({left: row.clientWidth * .85 * -1,\n        behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth'}); })()", ["callback"] : null }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])



    return(
        jsx("button",{...mergeSlotProps(rest, ({ "aria-controls":"anime_current", "aria-label":"Anteriores: Animes em destaque agora", className:"shelf-arrow", onClick:on_click_64b7b773124fbc6f016a96db7b9acc40, type:"button" }))},children)
    )
});
Button_button_2dc342d8e8986766ba5cbe91d652a2a9_3e8caf1e.displayName = "Button";
return Button_button_2dc342d8e8986766ba5cbe91d652a2a9_3e8caf1e;
})();

export const Button_button_1a68a11b32e211f84926001cad5cd57e_3e8caf1e = /*#__PURE__*/ (() => {
const Button_button_1a68a11b32e211f84926001cad5cd57e_3e8caf1e = memo(({children, ...rest}) => {
    const on_click_1113bd99c8ce0c3aba781bd7d562beee = useCallback(((_e) => (addEvents([(ReflexEvent("_call_script", ({ ["javascript_code"] : "(() => { const row = document.getElementById('anime_current');\n        if (row) row.scrollBy({left: row.clientWidth * .85 * 1,\n        behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth'}); })()", ["callback"] : null }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])



    return(
        jsx("button",{...mergeSlotProps(rest, ({ "aria-controls":"anime_current", "aria-label":"Pr\u00f3ximos: Animes em destaque agora", className:"shelf-arrow", onClick:on_click_1113bd99c8ce0c3aba781bd7d562beee, type:"button" }))},children)
    )
});
Button_button_1a68a11b32e211f84926001cad5cd57e_3e8caf1e.displayName = "Button";
return Button_button_1a68a11b32e211f84926001cad5cd57e_3e8caf1e;
})();

export const Foreach_comp_3fbc4ed77d686c3f43c44afc5484e387_3e8caf1e = /*#__PURE__*/ (() => {
const Foreach_comp_3fbc4ed77d686c3f43c44afc5484e387_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        Array.prototype.map.call(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.home_collections_rx_state_?.["anime_current"] ?? [],((m_rx_state_,index_rx_state_)=>(jsx("button",{className:"shelf-card",key:m_rx_state_?.["key"],onClick:((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.open_featured", ({ ["source"] : m_rx_state_?.["source"], ["identifier"] : m_rx_state_?.["external_id"], ["kind"] : "anime" }), ({  })))], [_e], ({  })))),type:"button"},jsx("div",{className:"shelf-poster"},jsx("div",{className:"cover-frame"},jsx("div",{"aria-hidden":true,className:"cover-placeholder"},jsx("span",{className:"cover-placeholder-brand"},"CODEBOXD"),jsx("div",{className:"cover-placeholder-copy"},jsx("span",{className:"cover-placeholder-label"},"Capa indispon\u00edvel"))),jsx(Fragment,{},(pyAnd(!((m_rx_state_?.["cover"]?.valueOf?.() === ""?.valueOf?.())), () => (!(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.failed_covers_rx_state_.includes(m_rx_state_?.["cover"]))))?(jsx(Fragment,{},jsx("img",{alt:m_rx_state_?.["title"],className:"media-cover",css:({ ["width"] : "100%", ["height"] : "100%" }),decoding:"async",loading:"lazy",onError:((...args) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.cover_failed", ({ ["url"] : m_rx_state_?.["cover"] }), ({  })))], args, ({  })))),src:m_rx_state_?.["cover"]},))):(jsx(Fragment,{},)))))),jsx("div",{className:"shelf-card-copy"},jsx("h3",{className:"shelf-card-title"},m_rx_state_?.["title"]),jsx("p",{className:"shelf-card-meta"},((m_rx_state_?.["kind"]+" \u00b7 ")+m_rx_state_?.["year"])))))))
    )
});
Foreach_comp_3fbc4ed77d686c3f43c44afc5484e387_3e8caf1e.displayName = "Foreach";
return Foreach_comp_3fbc4ed77d686c3f43c44afc5484e387_3e8caf1e;
})();

export const Bare_comp_07a16f13955a466226a65e32d61263ad_3e8caf1e = /*#__PURE__*/ (() => {
const Bare_comp_07a16f13955a466226a65e32d61263ad_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        (reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.home_collection_errors_rx_state_.includes("anime_current") ? "Esta sele\u00e7\u00e3o est\u00e1 indispon\u00edvel no momento." : "Ainda n\u00e3o h\u00e1 t\u00edtulos nesta sele\u00e7\u00e3o.")
    )
});
Bare_comp_07a16f13955a466226a65e32d61263ad_3e8caf1e.displayName = "Bare";
return Bare_comp_07a16f13955a466226a65e32d61263ad_3e8caf1e;
})();

export const Cond_comp_0208f1072b398198e34ee026670ce632_3e8caf1e = /*#__PURE__*/ (() => {
const Cond_comp_0208f1072b398198e34ee026670ce632_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        ((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.home_collections_rx_state_?.["anime_current"].length > 0)?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_0208f1072b398198e34ee026670ce632_3e8caf1e.displayName = "Cond";
return Cond_comp_0208f1072b398198e34ee026670ce632_3e8caf1e;
})();

export const Cond_comp_19911e358cf862da9dbf2841d81b5596_3e8caf1e = /*#__PURE__*/ (() => {
const Cond_comp_19911e358cf862da9dbf2841d81b5596_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        (!(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.search_active_rx_state_)?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_19911e358cf862da9dbf2841d81b5596_3e8caf1e.displayName = "Cond";
return Cond_comp_19911e358cf862da9dbf2841d81b5596_3e8caf1e;
})();

export const Button_button_593376f8f7c767ccd7d3c029f564cae9_3e8caf1e = /*#__PURE__*/ (() => {
const Button_button_593376f8f7c767ccd7d3c029f564cae9_3e8caf1e = memo(({children, ...rest}) => {
    const on_click_5c2f66104c1a55d4cbd2f2e8c82ff32c = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.more_results", ({  }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])
const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        jsx("button",{...mergeSlotProps(rest, ({ className:"action-button", disabled:reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.busy_rx_state_, onClick:on_click_5c2f66104c1a55d4cbd2f2e8c82ff32c, type:"button" }))},children)
    )
});
Button_button_593376f8f7c767ccd7d3c029f564cae9_3e8caf1e.displayName = "Button";
return Button_button_593376f8f7c767ccd7d3c029f564cae9_3e8caf1e;
})();

export const Cond_comp_817f15d08a631cdb805ff1bd92f20768_3e8caf1e = /*#__PURE__*/ (() => {
const Cond_comp_817f15d08a631cdb805ff1bd92f20768_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        (pyAnd(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.search_active_rx_state_, () => (reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.has_more_results_rx_state_))?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_817f15d08a631cdb805ff1bd92f20768_3e8caf1e.displayName = "Cond";
return Cond_comp_817f15d08a631cdb805ff1bd92f20768_3e8caf1e;
})();

export const Foreach_comp_5a2a41a2a417e865985403504195d4b0_3e8caf1e = /*#__PURE__*/ (() => {
const Foreach_comp_5a2a41a2a417e865985403504195d4b0_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        Array.prototype.map.call(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.catalog_items_rx_state_ ?? [],((m_rx_state_,index_2fd921edd9d56ecb4a361ae74ec5705f)=>(jsx(ReactRouterLink,{className:"media-card",key:index_2fd921edd9d56ecb4a361ae74ec5705f,to:("/obra/"+m_rx_state_?.["id"])},jsx("div",{className:"h-full"},jsx("div",{className:"cover-frame"},jsx("div",{"aria-hidden":true,className:"cover-placeholder"},jsx("span",{className:"cover-placeholder-brand"},"CODEBOXD"),jsx("div",{className:"cover-placeholder-copy"},jsx("span",{className:"cover-placeholder-label"},"Capa indispon\u00edvel"))),jsx(Fragment,{},(pyAnd(!((m_rx_state_?.["cover"]?.valueOf?.() === ""?.valueOf?.())), () => (!(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.failed_covers_rx_state_.includes(m_rx_state_?.["cover"]))))?(jsx(Fragment,{},jsx("img",{alt:m_rx_state_?.["title"],className:"media-cover",css:({ ["width"] : "100%", ["height"] : "100%" }),decoding:"async",loading:"lazy",onError:((...args) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.cover_failed", ({ ["url"] : m_rx_state_?.["cover"] }), ({  })))], args, ({  })))),src:m_rx_state_?.["cover"]},))):(jsx(Fragment,{},))))),jsx("div",{className:"p-4"},jsx("h3",{className:"font-semibold line-clamp-2"},m_rx_state_?.["title"]),jsx("p",{className:"text-sm text-gray-400 mt-3"},((m_rx_state_?.["kind"]+" \u00b7 ")+m_rx_state_?.["year"]))))))))
    )
});
Foreach_comp_5a2a41a2a417e865985403504195d4b0_3e8caf1e.displayName = "Foreach";
return Foreach_comp_5a2a41a2a417e865985403504195d4b0_3e8caf1e;
})();

export const Cond_comp_592313699e5b8de21bff2f69458eedc7_3e8caf1e = /*#__PURE__*/ (() => {
const Cond_comp_592313699e5b8de21bff2f69458eedc7_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        ((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.catalog_items_rx_state_.length > 0)?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_592313699e5b8de21bff2f69458eedc7_3e8caf1e.displayName = "Cond";
return Cond_comp_592313699e5b8de21bff2f69458eedc7_3e8caf1e;
})();

export const Img_img_960e481ba210164bc24e27a6763a0bdc_3e8caf1e = /*#__PURE__*/ (() => {
const Img_img_960e481ba210164bc24e27a6763a0bdc_3e8caf1e = memo(({children, ...rest}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        jsx("img",{...mergeSlotProps(rest, ({ alt:("Banner de "+reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.profile_rx_state_?.["display_name"]), className:"profile-banner-image", src:reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.profile_rx_state_?.["banner_url"] }))},)
    )
});
Img_img_960e481ba210164bc24e27a6763a0bdc_3e8caf1e.displayName = "Img";
return Img_img_960e481ba210164bc24e27a6763a0bdc_3e8caf1e;
})();

export const Cond_comp_bc31173616729c68d2f232f05b22ba63_3e8caf1e = /*#__PURE__*/ (() => {
const Cond_comp_bc31173616729c68d2f232f05b22ba63_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        (!((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.profile_rx_state_?.["banner_url"]?.valueOf?.() === ""?.valueOf?.()))?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_bc31173616729c68d2f232f05b22ba63_3e8caf1e.displayName = "Cond";
return Cond_comp_bc31173616729c68d2f232f05b22ba63_3e8caf1e;
})();

export const Img_img_87045e35e980de8cc27184c79f552550_3e8caf1e = /*#__PURE__*/ (() => {
const Img_img_87045e35e980de8cc27184c79f552550_3e8caf1e = memo(({children, ...rest}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        jsx("img",{...mergeSlotProps(rest, ({ alt:reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.profile_rx_state_?.["display_name"], className:"avatar", src:reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.profile_rx_state_?.["avatar_url"] }))},)
    )
});
Img_img_87045e35e980de8cc27184c79f552550_3e8caf1e.displayName = "Img";
return Img_img_87045e35e980de8cc27184c79f552550_3e8caf1e;
})();

export const Cond_comp_80078db4511cbc01773688633dadbf68_3e8caf1e = /*#__PURE__*/ (() => {
const Cond_comp_80078db4511cbc01773688633dadbf68_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        (!((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.profile_rx_state_?.["avatar_url"]?.valueOf?.() === ""?.valueOf?.()))?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_80078db4511cbc01773688633dadbf68_3e8caf1e.displayName = "Cond";
return Cond_comp_80078db4511cbc01773688633dadbf68_3e8caf1e;
})();

export const Bare_comp_619b6fb6ab6c096d7c5d7a0293cc393e_3e8caf1e = /*#__PURE__*/ (() => {
const Bare_comp_619b6fb6ab6c096d7c5d7a0293cc393e_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.profile_rx_state_?.["display_name"]
    )
});
Bare_comp_619b6fb6ab6c096d7c5d7a0293cc393e_3e8caf1e.displayName = "Bare";
return Bare_comp_619b6fb6ab6c096d7c5d7a0293cc393e_3e8caf1e;
})();

export const Bare_comp_ce38c55ba0b805dda85394000ed687d3_3e8caf1e = /*#__PURE__*/ (() => {
const Bare_comp_ce38c55ba0b805dda85394000ed687d3_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        ("@"+reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.profile_rx_state_?.["username"])
    )
});
Bare_comp_ce38c55ba0b805dda85394000ed687d3_3e8caf1e.displayName = "Bare";
return Bare_comp_ce38c55ba0b805dda85394000ed687d3_3e8caf1e;
})();

export const Bare_comp_cdfced3fa71fdb86024720334cd82d06_3e8caf1e = /*#__PURE__*/ (() => {
const Bare_comp_cdfced3fa71fdb86024720334cd82d06_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.profile_rx_state_?.["bio"]
    )
});
Bare_comp_cdfced3fa71fdb86024720334cd82d06_3e8caf1e.displayName = "Bare";
return Bare_comp_cdfced3fa71fdb86024720334cd82d06_3e8caf1e;
})();

export const Styledupload_comp_0d19de0736e1f8761409fc1ba92c36d9_3e8caf1e = /*#__PURE__*/ (() => {
const Styledupload_comp_0d19de0736e1f8761409fc1ba92c36d9_3e8caf1e = memo(({children}) => {
    const ref_profile_banner_upload = useRef(null); refs["ref_profile_banner_upload"] = ref_profile_banner_upload;
const [filesById, setFilesById] = useContext(UploadFilesContext);
const on_drop_7021fe1b08685bf503a9b970df95f421 = useCallback(((_ev_0) => ((e => setFilesById(filesById => {
    const updatedFilesById = Object.assign({}, filesById);
    updatedFilesById["profile_banner_upload"] = e;
    return updatedFilesById;
  })
    )(_ev_0))), [addEvents, ReflexEvent, filesById, setFilesById])
const on_drop_rejected_2fcedbdc0771e7617b4270e2d1ac8cc9 = useCallback(((_ev_0) => (addEvents([(ReflexEvent("_call_function", ({ ["function"] : (() => (refs['__toast']?.["error"]("", ({ ["title"] : "Files not Accepted", ["description"] : _ev_0.map(((osizayzf) => (osizayzf?.["file"]?.["path"]+": "+osizayzf?.["errors"].map(((wnkiegyk) => wnkiegyk?.["message"])).join(", ")))).join("\n\n"), ["closeButton"] : true, ["style"] : ({ ["whiteSpace"] : "pre-line" }) })))), ["callback"] : null }), ({  })))], [_ev_0], ({  })))), [addEvents, ReflexEvent])
const { getRootProps: xdvxrcsn, getInputProps: udaxihhe, isDragActive: bacghqta} = useDropzone(({ ["accept"] : ({ ["image/png"] : [".png"], ["image/jpeg"] : [".jpg", ".jpeg"], ["image/webp"] : [".webp"], ["image/gif"] : [".gif"] }), ["maxFiles"] : 1, ["maxSize"] : 5242880, ["multiple"] : true, ["id"] : "profile_banner_upload", ["onDrop"] : on_drop_7021fe1b08685bf503a9b970df95f421, ["onDropRejected"] : on_drop_rejected_2fcedbdc0771e7617b4270e2d1ac8cc9 }));



    return(
        jsx(Fragment,{},jsx("div",{className:"rx-Upload profile-upload-dropzone",css:({ ["border"] : "1px dashed var(--accent-12)", ["padding"] : "5em", ["textAlign"] : "center" }),id:"profile_banner_upload",ref:ref_profile_banner_upload,...xdvxrcsn()},jsx("input",{type:"file",...udaxihhe()},),jsx("div",{className:"profile-upload-prompt"},jsx(LucideImageUp,{size:18},),jsx("span",{},"Escolher ou arrastar uma imagem para o banner"))))
    )
});
Styledupload_comp_0d19de0736e1f8761409fc1ba92c36d9_3e8caf1e.displayName = "StyledUpload";
return Styledupload_comp_0d19de0736e1f8761409fc1ba92c36d9_3e8caf1e;
})();

export const Bare_comp_de7211f5cbb4c95725456f4dffe741aa_3e8caf1e = /*#__PURE__*/ (() => {
const Bare_comp_de7211f5cbb4c95725456f4dffe741aa_3e8caf1e = memo(({children}) => {
    const [filesById, setFilesById] = useContext(UploadFilesContext);



    return(
        (filesById["profile_banner_upload"] ? filesById["profile_banner_upload"].map((f) => f.name) : [])?.at?.(0)
    )
});
Bare_comp_de7211f5cbb4c95725456f4dffe741aa_3e8caf1e.displayName = "Bare";
return Bare_comp_de7211f5cbb4c95725456f4dffe741aa_3e8caf1e;
})();

export const Cond_comp_7f4325a35e58f10392284b8553d0c132_3e8caf1e = /*#__PURE__*/ (() => {
const Cond_comp_7f4325a35e58f10392284b8553d0c132_3e8caf1e = memo(({children}) => {
    const [filesById, setFilesById] = useContext(UploadFilesContext);



    return(
        (((filesById["profile_banner_upload"] ? filesById["profile_banner_upload"].map((f) => f.name) : []).length > 0)?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_7f4325a35e58f10392284b8553d0c132_3e8caf1e.displayName = "Cond";
return Cond_comp_7f4325a35e58f10392284b8553d0c132_3e8caf1e;
})();

export const Button_button_9373593b6bbbec522e31c0ceea88e582_3e8caf1e = /*#__PURE__*/ (() => {
const Button_button_9373593b6bbbec522e31c0ceea88e582_3e8caf1e = memo(({children, ...rest}) => {
    const [filesById, setFilesById] = useContext(UploadFilesContext);
const on_click_033087e95cb787663e2a9934b8e09f58 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.upload_profile_banner", ({ ["files"] : filesById?.["profile_banner_upload"], ["upload_param_name"] : "files", ["upload_id"] : "profile_banner_upload", ["extra_headers"] : ({  }) }), ({  }), "uploadFiles"))], [_e], ({  })))), [addEvents, ReflexEvent, filesById, setFilesById])



    return(
        jsx("button",{...mergeSlotProps(rest, ({ className:"action-button", onClick:on_click_033087e95cb787663e2a9934b8e09f58, type:"button" }))},children)
    )
});
Button_button_9373593b6bbbec522e31c0ceea88e582_3e8caf1e.displayName = "Button";
return Button_button_9373593b6bbbec522e31c0ceea88e582_3e8caf1e;
})();

export const Cond_comp_c7af4212f237dd58d52d15533fac7158_3e8caf1e = /*#__PURE__*/ (() => {
const Cond_comp_c7af4212f237dd58d52d15533fac7158_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        (reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.owns_profile_rx_state_?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_c7af4212f237dd58d52d15533fac7158_3e8caf1e.displayName = "Cond";
return Cond_comp_c7af4212f237dd58d52d15533fac7158_3e8caf1e;
})();

export const Input_input_50e2a4d7eae0f1067d1240fd2f38dbab_3e8caf1e = /*#__PURE__*/ (() => {
const Input_input_50e2a4d7eae0f1067d1240fd2f38dbab_3e8caf1e = memo(({children, ...rest}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        jsx("input",{...mergeSlotProps(rest, ({ className:"w-full rounded-xl border border-white/15 bg-[#151719] px-4 py-3 text-white", defaultValue:reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.profile_rx_state_?.["username"], maxLength:30, name:"username", pattern:"[a-z0-9_]{3,30}", required:true }))},)
    )
});
Input_input_50e2a4d7eae0f1067d1240fd2f38dbab_3e8caf1e.displayName = "Input";
return Input_input_50e2a4d7eae0f1067d1240fd2f38dbab_3e8caf1e;
})();

export const Input_input_940691c5b7c0af388e3a208ede9e0f92_3e8caf1e = /*#__PURE__*/ (() => {
const Input_input_940691c5b7c0af388e3a208ede9e0f92_3e8caf1e = memo(({children, ...rest}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        jsx("input",{...mergeSlotProps(rest, ({ className:"w-full rounded-xl border border-white/15 bg-[#151719] px-4 py-3 text-white", defaultValue:reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.profile_rx_state_?.["display_name"], maxLength:80, name:"display_name", required:true }))},)
    )
});
Input_input_940691c5b7c0af388e3a208ede9e0f92_3e8caf1e.displayName = "Input";
return Input_input_940691c5b7c0af388e3a208ede9e0f92_3e8caf1e;
})();

export const Textarea_textarea_fc41a488d4bca24389529bc5d66f2c5c_3e8caf1e = /*#__PURE__*/ (() => {
const Textarea_textarea_fc41a488d4bca24389529bc5d66f2c5c_3e8caf1e = memo(({children, ...rest}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        jsx("textarea",{...mergeSlotProps(rest, ({ className:"w-full rounded-xl border border-white/15 bg-[#151719] px-4 py-3 text-white", defaultValue:reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.profile_rx_state_?.["bio"], maxLength:1000, name:"bio" }))},)
    )
});
Textarea_textarea_fc41a488d4bca24389529bc5d66f2c5c_3e8caf1e.displayName = "Textarea";
return Textarea_textarea_fc41a488d4bca24389529bc5d66f2c5c_3e8caf1e;
})();

export const Input_input_bff7385a7a25cfe106e8145ba86df766_3e8caf1e = /*#__PURE__*/ (() => {
const Input_input_bff7385a7a25cfe106e8145ba86df766_3e8caf1e = memo(({children, ...rest}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        jsx("input",{...mergeSlotProps(rest, ({ className:"w-full rounded-xl border border-white/15 bg-[#151719] px-4 py-3 text-white", defaultValue:reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.profile_rx_state_?.["avatar_url"], name:"avatar_url", type:"url" }))},)
    )
});
Input_input_bff7385a7a25cfe106e8145ba86df766_3e8caf1e.displayName = "Input";
return Input_input_bff7385a7a25cfe106e8145ba86df766_3e8caf1e;
})();

export const Form_form_fcf98ecf51950d2225ae0a69e4c74998_3e8caf1e = /*#__PURE__*/ (() => {
const Form_form_fcf98ecf51950d2225ae0a69e4c74998_3e8caf1e = memo(({children, ...rest}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)

    const handleSubmit_1bc5cdbac55f7a92349a2d1c557af138 = useCallback((ev) => {
        const $form = ev.target
        ev.preventDefault()
        const form_data = {...Object.fromEntries(new FormData($form).entries()), ...({  })};

        (((...args) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.save_profile", ({ ["form"] : form_data }), ({  })))], args, ({  }))))(ev));

        if (false) {
            $form.reset()
        }
    })
    


    return(
        jsx("form",{...mergeSlotProps(rest, ({ className:"editor-form", key:reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.profile_rx_state_?.["username"], onSubmit:handleSubmit_1bc5cdbac55f7a92349a2d1c557af138 }))},children)
    )
});
Form_form_fcf98ecf51950d2225ae0a69e4c74998_3e8caf1e.displayName = "Form";
return Form_form_fcf98ecf51950d2225ae0a69e4c74998_3e8caf1e;
})();

export const Bare_comp_540a1c870ac2306fd3819aeda8028b07_3e8caf1e = /*#__PURE__*/ (() => {
const Bare_comp_540a1c870ac2306fd3819aeda8028b07_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        (reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.following_ids_rx_state_.includes(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.profile_rx_state_?.["user_id"]) ? "Deixar de seguir" : "Seguir")
    )
});
Bare_comp_540a1c870ac2306fd3819aeda8028b07_3e8caf1e.displayName = "Bare";
return Bare_comp_540a1c870ac2306fd3819aeda8028b07_3e8caf1e;
})();

export const Button_button_0c8ebfbe37a0719ca70ad1bd6a1df42e_3e8caf1e = /*#__PURE__*/ (() => {
const Button_button_0c8ebfbe37a0719ca70ad1bd6a1df42e_3e8caf1e = memo(({children, ...rest}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)
const on_click_57f4377352c30294f0af654f002579ed = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.follow", ({ ["uid"] : reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.profile_rx_state_?.["user_id"] }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent, reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state])



    return(
        jsx("button",{...mergeSlotProps(rest, ({ className:"action-button", onClick:on_click_57f4377352c30294f0af654f002579ed, type:"button" }))},children)
    )
});
Button_button_0c8ebfbe37a0719ca70ad1bd6a1df42e_3e8caf1e.displayName = "Button";
return Button_button_0c8ebfbe37a0719ca70ad1bd6a1df42e_3e8caf1e;
})();

export const Button_button_565fc52abe9b26c8818d6f39cd47533c_3e8caf1e = /*#__PURE__*/ (() => {
const Button_button_565fc52abe9b26c8818d6f39cd47533c_3e8caf1e = memo(({children, ...rest}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)
const on_click_454da6800a09ad9ed7f52dfda1af67c9 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.open_report", ({ ["target_type"] : "profile", ["target_id"] : reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.profile_rx_state_?.["user_id"] }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent, reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state])



    return(
        jsx("button",{...mergeSlotProps(rest, ({ className:"action-button", onClick:on_click_454da6800a09ad9ed7f52dfda1af67c9, type:"button" }))},children)
    )
});
Button_button_565fc52abe9b26c8818d6f39cd47533c_3e8caf1e.displayName = "Button";
return Button_button_565fc52abe9b26c8818d6f39cd47533c_3e8caf1e;
})();

export const Cond_comp_8cb428571a8d7c34ea8007b92a3f7e79_3e8caf1e = /*#__PURE__*/ (() => {
const Cond_comp_8cb428571a8d7c34ea8007b92a3f7e79_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)
const reflex___state____state__codeboxd_main___state___session____session_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state)



    return(
        (!((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.profile_rx_state_?.["user_id"]?.valueOf?.() === (JSON.stringify(reflex___state____state__codeboxd_main___state___session____session_state.user_id_rx_state_))?.valueOf?.()))?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_8cb428571a8d7c34ea8007b92a3f7e79_3e8caf1e.displayName = "Cond";
return Cond_comp_8cb428571a8d7c34ea8007b92a3f7e79_3e8caf1e;
})();

export const Bare_comp_c985820f048f13fe2f8fc14b33cf1ce3_3e8caf1e = /*#__PURE__*/ (() => {
const Bare_comp_c985820f048f13fe2f8fc14b33cf1ce3_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.followers_rx_state_.length
    )
});
Bare_comp_c985820f048f13fe2f8fc14b33cf1ce3_3e8caf1e.displayName = "Bare";
return Bare_comp_c985820f048f13fe2f8fc14b33cf1ce3_3e8caf1e;
})();

export const Bare_comp_e6cec44425b0dc82c8bde433a4c585cc_3e8caf1e = /*#__PURE__*/ (() => {
const Bare_comp_e6cec44425b0dc82c8bde433a4c585cc_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.following_rx_state_.length
    )
});
Bare_comp_e6cec44425b0dc82c8bde433a4c585cc_3e8caf1e.displayName = "Bare";
return Bare_comp_e6cec44425b0dc82c8bde433a4c585cc_3e8caf1e;
})();

export const Bare_comp_4589edba2f75b6922114c07a2119b289_3e8caf1e = /*#__PURE__*/ (() => {
const Bare_comp_4589edba2f75b6922114c07a2119b289_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.profile_activity_rx_state_.length
    )
});
Bare_comp_4589edba2f75b6922114c07a2119b289_3e8caf1e.displayName = "Bare";
return Bare_comp_4589edba2f75b6922114c07a2119b289_3e8caf1e;
})();

export const Foreach_comp_8c22014173e49116b5c0576d11b1e216_3e8caf1e = /*#__PURE__*/ (() => {
const Foreach_comp_8c22014173e49116b5c0576d11b1e216_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        Array.prototype.map.call(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.profile_activity_rx_state_ ?? [],((i_rx_state_,index_2ef475f95355dadd562ead256c35aaf4)=>(jsx("article",{className:"activity-card",key:index_2ef475f95355dadd562ead256c35aaf4},jsx(ReactRouterLink,{className:"activity-cover",to:("/obra/"+i_rx_state_?.["id"])},jsx(Fragment,{},(!((i_rx_state_?.["cover"]?.valueOf?.() === ""?.valueOf?.()))?(jsx(Fragment,{},jsx("img",{alt:i_rx_state_?.["title"],loading:"lazy",src:i_rx_state_?.["cover"]},))):(jsx(Fragment,{},jsx(LucideBookOpen,{size:28},)))))),jsx("div",{className:"min-w-0"},jsx(ReactRouterLink,{className:"font-semibold",to:("/obra/"+i_rx_state_?.["id"])},i_rx_state_?.["title"]),jsx("p",{className:"activity-meta"},((((i_rx_state_?.["kind"]+" \u00b7 ")+i_rx_state_?.["status"])+" \u00b7 ")+i_rx_state_?.["rating"])),jsx(Fragment,{},((i_rx_state_?.["spoiler"]?.valueOf?.() === "True"?.valueOf?.())?(jsx(Fragment,{},jsx("details",{},jsx("summary",{className:"cursor-pointer text-amber-300"},"Mostrar conte\u00fado com spoilers"),jsx("p",{className:"whitespace-pre-wrap mt-3"},i_rx_state_?.["review"])))):(jsx(Fragment,{},jsx("p",{className:"whitespace-pre-wrap"},i_rx_state_?.["review"]))))))))))
    )
});
Foreach_comp_8c22014173e49116b5c0576d11b1e216_3e8caf1e.displayName = "Foreach";
return Foreach_comp_8c22014173e49116b5c0576d11b1e216_3e8caf1e;
})();

export const Cond_comp_7513c695415c27b4ed43eae16e4a8902_3e8caf1e = /*#__PURE__*/ (() => {
const Cond_comp_7513c695415c27b4ed43eae16e4a8902_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        ((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.profile_activity_rx_state_.length > 0)?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_7513c695415c27b4ed43eae16e4a8902_3e8caf1e.displayName = "Cond";
return Cond_comp_7513c695415c27b4ed43eae16e4a8902_3e8caf1e;
})();

export const Foreach_comp_40491880d3d5dbeacdadd7a3b1b9b5e9_3e8caf1e = /*#__PURE__*/ (() => {
const Foreach_comp_40491880d3d5dbeacdadd7a3b1b9b5e9_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)
const reflex___state____state__codeboxd_main___state___session____session_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state)



    return(
        Array.prototype.map.call(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.followers_rx_state_ ?? [],((p_rx_state_,index_e0d187db7a257ea520f63a3a836a1e66)=>(jsx("article",{className:"rounded-2xl border border-white/10 bg-[#111114] p-5 space-y-4",key:index_e0d187db7a257ea520f63a3a836a1e66},jsx(ReactRouterLink,{className:"text-xl font-semibold",to:("/perfil/"+p_rx_state_?.["user_id"])},p_rx_state_?.["display_name"]),jsx("p",{className:"text-[#F5B300]"},("@"+p_rx_state_?.["username"])),jsx("p",{className:"text-gray-400"},p_rx_state_?.["bio"]),jsx(Fragment,{},(pyAnd(reflex___state____state__codeboxd_main___state___session____session_state.is_authenticated_rx_state_, () => (!((p_rx_state_?.["user_id"]?.valueOf?.() === (JSON.stringify(reflex___state____state__codeboxd_main___state___session____session_state.user_id_rx_state_))?.valueOf?.()))))?(jsx(Fragment,{},jsx("button",{className:"action-button",onClick:((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.follow", ({ ["uid"] : p_rx_state_?.["user_id"] }), ({  })))], [_e], ({  })))),type:"button"},(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.following_ids_rx_state_.includes(p_rx_state_?.["user_id"]) ? "Deixar de seguir" : "Seguir")))):(jsx(Fragment,{},))))))))
    )
});
Foreach_comp_40491880d3d5dbeacdadd7a3b1b9b5e9_3e8caf1e.displayName = "Foreach";
return Foreach_comp_40491880d3d5dbeacdadd7a3b1b9b5e9_3e8caf1e;
})();

export const Cond_comp_3218fc2696756ca4bd3001527b4d7762_3e8caf1e = /*#__PURE__*/ (() => {
const Cond_comp_3218fc2696756ca4bd3001527b4d7762_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        ((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.followers_rx_state_.length > 0)?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_3218fc2696756ca4bd3001527b4d7762_3e8caf1e.displayName = "Cond";
return Cond_comp_3218fc2696756ca4bd3001527b4d7762_3e8caf1e;
})();

export const Foreach_comp_eecbe7dcdb01e934ef5124e83a74ced5_3e8caf1e = /*#__PURE__*/ (() => {
const Foreach_comp_eecbe7dcdb01e934ef5124e83a74ced5_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)
const reflex___state____state__codeboxd_main___state___session____session_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state)



    return(
        Array.prototype.map.call(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.following_rx_state_ ?? [],((p_rx_state_,index_e0d187db7a257ea520f63a3a836a1e66)=>(jsx("article",{className:"rounded-2xl border border-white/10 bg-[#111114] p-5 space-y-4",key:index_e0d187db7a257ea520f63a3a836a1e66},jsx(ReactRouterLink,{className:"text-xl font-semibold",to:("/perfil/"+p_rx_state_?.["user_id"])},p_rx_state_?.["display_name"]),jsx("p",{className:"text-[#F5B300]"},("@"+p_rx_state_?.["username"])),jsx("p",{className:"text-gray-400"},p_rx_state_?.["bio"]),jsx(Fragment,{},(pyAnd(reflex___state____state__codeboxd_main___state___session____session_state.is_authenticated_rx_state_, () => (!((p_rx_state_?.["user_id"]?.valueOf?.() === (JSON.stringify(reflex___state____state__codeboxd_main___state___session____session_state.user_id_rx_state_))?.valueOf?.()))))?(jsx(Fragment,{},jsx("button",{className:"action-button",onClick:((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.follow", ({ ["uid"] : p_rx_state_?.["user_id"] }), ({  })))], [_e], ({  })))),type:"button"},(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.following_ids_rx_state_.includes(p_rx_state_?.["user_id"]) ? "Deixar de seguir" : "Seguir")))):(jsx(Fragment,{},))))))))
    )
});
Foreach_comp_eecbe7dcdb01e934ef5124e83a74ced5_3e8caf1e.displayName = "Foreach";
return Foreach_comp_eecbe7dcdb01e934ef5124e83a74ced5_3e8caf1e;
})();

export const Cond_comp_ecda19cb6df000be0421db513c006482_3e8caf1e = /*#__PURE__*/ (() => {
const Cond_comp_ecda19cb6df000be0421db513c006482_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        ((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.following_rx_state_.length > 0)?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_ecda19cb6df000be0421db513c006482_3e8caf1e.displayName = "Cond";
return Cond_comp_ecda19cb6df000be0421db513c006482_3e8caf1e;
})();

export const Select_select_897bff1adfd00cde4ced1d2b78a7dc3e_3e8caf1e = /*#__PURE__*/ (() => {
const Select_select_897bff1adfd00cde4ced1d2b78a7dc3e_3e8caf1e = memo(({children, ...rest}) => {
    const ref_report_reason = useRef(null); refs["ref_report_reason"] = ref_report_reason;
const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        jsx("select",{...mergeSlotProps(rest, ({ className:"w-full rounded-xl border border-white/15 bg-[#151719] px-4 py-3 text-white", defaultValue:reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.report_reason_rx_state_, id:"report-reason", name:"reason", ref:ref_report_reason }))},children)
    )
});
Select_select_897bff1adfd00cde4ced1d2b78a7dc3e_3e8caf1e.displayName = "Select";
return Select_select_897bff1adfd00cde4ced1d2b78a7dc3e_3e8caf1e;
})();

export const Button_button_904143455391aa9a489b5502b9b71a51_3e8caf1e = /*#__PURE__*/ (() => {
const Button_button_904143455391aa9a489b5502b9b71a51_3e8caf1e = memo(({children, ...rest}) => {
    const on_click_a2e4e7fb8948596b9268fa2b1b074334 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.close_report", ({  }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])
const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        jsx("button",{...mergeSlotProps(rest, ({ className:"quiet-button", disabled:reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.report_sending_rx_state_, onClick:on_click_a2e4e7fb8948596b9268fa2b1b074334, type:"button" }))},children)
    )
});
Button_button_904143455391aa9a489b5502b9b71a51_3e8caf1e.displayName = "Button";
return Button_button_904143455391aa9a489b5502b9b71a51_3e8caf1e;
})();

export const Bare_comp_56fa90ba9241804f0e6d47b76a86bcc0_3e8caf1e = /*#__PURE__*/ (() => {
const Bare_comp_56fa90ba9241804f0e6d47b76a86bcc0_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        (reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.report_sending_rx_state_ ? "Enviando\u2026" : "Enviar report")
    )
});
Bare_comp_56fa90ba9241804f0e6d47b76a86bcc0_3e8caf1e.displayName = "Bare";
return Bare_comp_56fa90ba9241804f0e6d47b76a86bcc0_3e8caf1e;
})();

export const Button_button_35e01cb58b1e8950812def4922466b50_3e8caf1e = /*#__PURE__*/ (() => {
const Button_button_35e01cb58b1e8950812def4922466b50_3e8caf1e = memo(({children, ...rest}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        jsx("button",{...mergeSlotProps(rest, ({ className:"action-button", disabled:reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.report_sending_rx_state_, type:"submit" }))},children)
    )
});
Button_button_35e01cb58b1e8950812def4922466b50_3e8caf1e.displayName = "Button";
return Button_button_35e01cb58b1e8950812def4922466b50_3e8caf1e;
})();

export const Form_form_3c91a8aef990ee65228bf202ed864429_3e8caf1e = /*#__PURE__*/ (() => {
const Form_form_3c91a8aef990ee65228bf202ed864429_3e8caf1e = memo(({children, ...rest}) => {
    

    const handleSubmit_c34c039c29c12f5ea559f50a3685a8db = useCallback((ev) => {
        const $form = ev.target
        ev.preventDefault()
        const form_data = {...Object.fromEntries(new FormData($form).entries()), ...({ ["report_reason"] : getRefValue(refs["ref_report_reason"]), ["report_description"] : getRefValue(refs["ref_report_description"]) })};

        (((...args) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.submit_report", ({ ["form"] : form_data }), ({  })))], args, ({  }))))(ev));

        if (false) {
            $form.reset()
        }
    })
    


    return(
        jsx("form",{...mergeSlotProps(rest, ({ className:"space-y-3", onSubmit:handleSubmit_c34c039c29c12f5ea559f50a3685a8db }))},children)
    )
});
Form_form_3c91a8aef990ee65228bf202ed864429_3e8caf1e.displayName = "Form";
return Form_form_3c91a8aef990ee65228bf202ed864429_3e8caf1e;
})();

export const Cond_comp_f5ad90b63d62e42141f6bb5cff85591e_3e8caf1e = /*#__PURE__*/ (() => {
const Cond_comp_f5ad90b63d62e42141f6bb5cff85591e_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        (reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.report_dialog_open_rx_state_?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_f5ad90b63d62e42141f6bb5cff85591e_3e8caf1e.displayName = "Cond";
return Cond_comp_f5ad90b63d62e42141f6bb5cff85591e_3e8caf1e;
})();

export const Styledupload_comp_886bfafb3ed97eaa87558d8065b9a04d_3e8caf1e = /*#__PURE__*/ (() => {
const Styledupload_comp_886bfafb3ed97eaa87558d8065b9a04d_3e8caf1e = memo(({children}) => {
    const ref_profile_banner_upload = useRef(null); refs["ref_profile_banner_upload"] = ref_profile_banner_upload;
const [filesById, setFilesById] = useContext(UploadFilesContext);
const on_drop_7021fe1b08685bf503a9b970df95f421 = useCallback(((_ev_0) => ((e => setFilesById(filesById => {
    const updatedFilesById = Object.assign({}, filesById);
    updatedFilesById["profile_banner_upload"] = e;
    return updatedFilesById;
  })
    )(_ev_0))), [addEvents, ReflexEvent, filesById, setFilesById])
const on_drop_rejected_51f7597a906ee6a527ceb347e5723946 = useCallback(((_ev_0) => (addEvents([(ReflexEvent("_call_function", ({ ["function"] : (() => (refs['__toast']?.["error"]("", ({ ["title"] : "Files not Accepted", ["description"] : _ev_0.map(((dmioulfl) => (dmioulfl?.["file"]?.["path"]+": "+dmioulfl?.["errors"].map(((lgviwvuc) => lgviwvuc?.["message"])).join(", ")))).join("\n\n"), ["closeButton"] : true, ["style"] : ({ ["whiteSpace"] : "pre-line" }) })))), ["callback"] : null }), ({  })))], [_ev_0], ({  })))), [addEvents, ReflexEvent])
const { getRootProps: zbxordmc, getInputProps: dcmdllti, isDragActive: rjutlsgw} = useDropzone(({ ["accept"] : ({ ["image/png"] : [".png"], ["image/jpeg"] : [".jpg", ".jpeg"], ["image/webp"] : [".webp"], ["image/gif"] : [".gif"] }), ["maxFiles"] : 1, ["maxSize"] : 5242880, ["multiple"] : true, ["id"] : "profile_banner_upload", ["onDrop"] : on_drop_7021fe1b08685bf503a9b970df95f421, ["onDropRejected"] : on_drop_rejected_51f7597a906ee6a527ceb347e5723946 }));



    return(
        jsx(Fragment,{},jsx("div",{className:"rx-Upload profile-upload-dropzone",css:({ ["border"] : "1px dashed var(--accent-12)", ["padding"] : "5em", ["textAlign"] : "center" }),id:"profile_banner_upload",ref:ref_profile_banner_upload,...zbxordmc()},jsx("input",{type:"file",...dcmdllti()},),jsx("div",{className:"profile-upload-prompt"},jsx(LucideImageUp,{size:18},),jsx("span",{},"Escolher ou arrastar uma imagem para o banner"))))
    )
});
Styledupload_comp_886bfafb3ed97eaa87558d8065b9a04d_3e8caf1e.displayName = "StyledUpload";
return Styledupload_comp_886bfafb3ed97eaa87558d8065b9a04d_3e8caf1e;
})();

export const Img_img_c5019e18dca4bce5bc18fa154dacb897_3e8caf1e = /*#__PURE__*/ (() => {
const Img_img_c5019e18dca4bce5bc18fa154dacb897_3e8caf1e = memo(({children, ...rest}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        jsx("img",{...mergeSlotProps(rest, ({ alt:("Capa de "+reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.selected_rx_state_?.["title"]), className:"media-detail-poster", src:reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.selected_rx_state_?.["cover"] }))},)
    )
});
Img_img_c5019e18dca4bce5bc18fa154dacb897_3e8caf1e.displayName = "Img";
return Img_img_c5019e18dca4bce5bc18fa154dacb897_3e8caf1e;
})();

export const Cond_comp_9bae289fc21750cd6aa9a49647ce6bc8_3e8caf1e = /*#__PURE__*/ (() => {
const Cond_comp_9bae289fc21750cd6aa9a49647ce6bc8_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        (!((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.selected_rx_state_?.["cover"]?.valueOf?.() === ""?.valueOf?.()))?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_9bae289fc21750cd6aa9a49647ce6bc8_3e8caf1e.displayName = "Cond";
return Cond_comp_9bae289fc21750cd6aa9a49647ce6bc8_3e8caf1e;
})();

export const Img_img_b60c020db59092617e0b927e21173350_3e8caf1e = /*#__PURE__*/ (() => {
const Img_img_b60c020db59092617e0b927e21173350_3e8caf1e = memo(({children, ...rest}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        jsx("img",{...mergeSlotProps(rest, ({ alt:"", "aria-hidden":true, className:"media-detail-backdrop", src:reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.selected_rx_state_?.["backdrop"] }))},)
    )
});
Img_img_b60c020db59092617e0b927e21173350_3e8caf1e.displayName = "Img";
return Img_img_b60c020db59092617e0b927e21173350_3e8caf1e;
})();

export const Cond_comp_1918a2fcefb5329a1560a39b1a30c16b_3e8caf1e = /*#__PURE__*/ (() => {
const Cond_comp_1918a2fcefb5329a1560a39b1a30c16b_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        (!((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.selected_rx_state_?.["backdrop"]?.valueOf?.() === ""?.valueOf?.()))?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_1918a2fcefb5329a1560a39b1a30c16b_3e8caf1e.displayName = "Cond";
return Cond_comp_1918a2fcefb5329a1560a39b1a30c16b_3e8caf1e;
})();

export const Bare_comp_9b05edd3aecbe40c09810d78470c3e82_3e8caf1e = /*#__PURE__*/ (() => {
const Bare_comp_9b05edd3aecbe40c09810d78470c3e82_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        ((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.selected_rx_state_?.["kind"]+"  \u00b7  ")+reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.selected_rx_state_?.["year"])
    )
});
Bare_comp_9b05edd3aecbe40c09810d78470c3e82_3e8caf1e.displayName = "Bare";
return Bare_comp_9b05edd3aecbe40c09810d78470c3e82_3e8caf1e;
})();

export const Bare_comp_8ccda70b87a83dddfc57e5700244cbd8_3e8caf1e = /*#__PURE__*/ (() => {
const Bare_comp_8ccda70b87a83dddfc57e5700244cbd8_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.selected_rx_state_?.["title"]
    )
});
Bare_comp_8ccda70b87a83dddfc57e5700244cbd8_3e8caf1e.displayName = "Bare";
return Bare_comp_8ccda70b87a83dddfc57e5700244cbd8_3e8caf1e;
})();

export const Bare_comp_4425e26a5a192c30fc6fcc50d60262c2_3e8caf1e = /*#__PURE__*/ (() => {
const Bare_comp_4425e26a5a192c30fc6fcc50d60262c2_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        (!((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.selected_rx_state_?.["description"]?.valueOf?.() === ""?.valueOf?.())) ? reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.selected_rx_state_?.["description"] : "Descri\u00e7\u00e3o ainda n\u00e3o dispon\u00edvel.")
    )
});
Bare_comp_4425e26a5a192c30fc6fcc50d60262c2_3e8caf1e.displayName = "Bare";
return Bare_comp_4425e26a5a192c30fc6fcc50d60262c2_3e8caf1e;
})();

export const Button_button_83e1f6675e1568b3ee80b4e84bc8b500_3e8caf1e = /*#__PURE__*/ (() => {
const Button_button_83e1f6675e1568b3ee80b4e84bc8b500_3e8caf1e = memo(({children, ...rest}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)
const on_click_c63fe4ea54a340c4b2dcabcaf3c79a95 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.open_report", ({ ["target_type"] : "media", ["target_id"] : reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.selected_rx_state_?.["id"] }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent, reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state])



    return(
        jsx("button",{...mergeSlotProps(rest, ({ className:"action-button", onClick:on_click_c63fe4ea54a340c4b2dcabcaf3c79a95, type:"button" }))},children)
    )
});
Button_button_83e1f6675e1568b3ee80b4e84bc8b500_3e8caf1e.displayName = "Button";
return Button_button_83e1f6675e1568b3ee80b4e84bc8b500_3e8caf1e;
})();

export const Bare_comp_916976caf1486ae985b4f8b3a54715c4_3e8caf1e = /*#__PURE__*/ (() => {
const Bare_comp_916976caf1486ae985b4f8b3a54715c4_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        (!((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.selected_rx_state_?.["details"]?.valueOf?.() === ""?.valueOf?.())) ? ((((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.selected_rx_state_?.["details"]+"  \u00b7  ")+reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.selected_rx_state_?.["kind"])+"  \u00b7  ")+reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.selected_rx_state_?.["year"]) : ((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.selected_rx_state_?.["kind"]+"  \u00b7  ")+reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.selected_rx_state_?.["year"]))
    )
});
Bare_comp_916976caf1486ae985b4f8b3a54715c4_3e8caf1e.displayName = "Bare";
return Bare_comp_916976caf1486ae985b4f8b3a54715c4_3e8caf1e;
})();

export const Foreach_comp_4d07be8dd44886d60d10dd0764ea9810_3e8caf1e = /*#__PURE__*/ (() => {
const Foreach_comp_4d07be8dd44886d60d10dd0764ea9810_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        Array.prototype.map.call(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.availability_rx_state_ ?? [],((provider_rx_state_,index_a560ab07e6b05611624fbf2495b07511)=>(jsx(ReactRouterLink,{className:"availability-chip",key:index_a560ab07e6b05611624fbf2495b07511,rel:"noopener noreferrer",target:"_blank",to:provider_rx_state_?.["url"]},jsx("span",{},provider_rx_state_?.["name"])))))
    )
});
Foreach_comp_4d07be8dd44886d60d10dd0764ea9810_3e8caf1e.displayName = "Foreach";
return Foreach_comp_4d07be8dd44886d60d10dd0764ea9810_3e8caf1e;
})();

export const Cond_comp_d95f2c924a908b82414b111eb3056b23_3e8caf1e = /*#__PURE__*/ (() => {
const Cond_comp_d95f2c924a908b82414b111eb3056b23_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        ((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.availability_rx_state_.length > 0)?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_d95f2c924a908b82414b111eb3056b23_3e8caf1e.displayName = "Cond";
return Cond_comp_d95f2c924a908b82414b111eb3056b23_3e8caf1e;
})();

export const Cond_comp_547c94e2ebc8ce9506ae9c36452160a4_3e8caf1e = /*#__PURE__*/ (() => {
const Cond_comp_547c94e2ebc8ce9506ae9c36452160a4_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        ((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.selected_rx_state_?.["source"]?.valueOf?.() === "tmdb"?.valueOf?.())?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_547c94e2ebc8ce9506ae9c36452160a4_3e8caf1e.displayName = "Cond";
return Cond_comp_547c94e2ebc8ce9506ae9c36452160a4_3e8caf1e;
})();

export const Foreach_comp_25b3855d7833aaa13670982e217d23a5_3e8caf1e = /*#__PURE__*/ (() => {
const Foreach_comp_25b3855d7833aaa13670982e217d23a5_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        Array.prototype.map.call(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.trailers_rx_state_ ?? [],((trailer_rx_state_,index_073fa740abff50f3f7bfaf22a08f17f2)=>(jsx("article",{className:"media-trailer-card",key:index_073fa740abff50f3f7bfaf22a08f17f2},jsx("h3",{className:"font-semibold mb-3"},trailer_rx_state_?.["title"]),jsx("iframe",{allow:"accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share",className:"media-trailer",css:({ ["allowFullscreen"] : true }),loading:"lazy",src:trailer_rx_state_?.["embed_url"],title:trailer_rx_state_?.["title"]},)))))
    )
});
Foreach_comp_25b3855d7833aaa13670982e217d23a5_3e8caf1e.displayName = "Foreach";
return Foreach_comp_25b3855d7833aaa13670982e217d23a5_3e8caf1e;
})();

export const Cond_comp_d57b8070a9feb29ca6cd4fc1aaa30dd3_3e8caf1e = /*#__PURE__*/ (() => {
const Cond_comp_d57b8070a9feb29ca6cd4fc1aaa30dd3_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        ((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.trailers_rx_state_.length > 0)?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_d57b8070a9feb29ca6cd4fc1aaa30dd3_3e8caf1e.displayName = "Cond";
return Cond_comp_d57b8070a9feb29ca6cd4fc1aaa30dd3_3e8caf1e;
})();

export const Input_input_8eee4e7c7bf30df751b5f981a2b54039_3e8caf1e = /*#__PURE__*/ (() => {
const Input_input_8eee4e7c7bf30df751b5f981a2b54039_3e8caf1e = memo(({children, ...rest}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        jsx("input",{...mergeSlotProps(rest, ({ name:"status", type:"hidden", value:(isNotNullOrUndefined(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.selected_status_rx_state_) ? reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.selected_status_rx_state_ : "") }))},)
    )
});
Input_input_8eee4e7c7bf30df751b5f981a2b54039_3e8caf1e.displayName = "Input";
return Input_input_8eee4e7c7bf30df751b5f981a2b54039_3e8caf1e;
})();

export const Foreach_comp_3376754981f7d46da0576e10df962641_3e8caf1e = /*#__PURE__*/ (() => {
const Foreach_comp_3376754981f7d46da0576e10df962641_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        Array.prototype.map.call([["planned", "Quero ver / ler"], ["in_progress", "Em andamento"], ["completed", "Conclu\u00eddo"], ["dropped", "Abandonado"]] ?? [],((pair_rx_state_,index_d1bb38ce5faf2c9570b5bce241b99a6d)=>(jsx("button",{className:((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.selected_status_rx_state_?.valueOf?.() === pair_rx_state_?.at?.(0)?.valueOf?.()) ? "status-chip selected" : "status-chip"),key:index_d1bb38ce5faf2c9570b5bce241b99a6d,onClick:((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.set_selected_status", ({ ["value"] : pair_rx_state_?.at?.(0) }), ({  })))], [_e], ({  })))),type:"button"},pair_rx_state_?.at?.(1)))))
    )
});
Foreach_comp_3376754981f7d46da0576e10df962641_3e8caf1e.displayName = "Foreach";
return Foreach_comp_3376754981f7d46da0576e10df962641_3e8caf1e;
})();

export const Button_button_899cbce24fd6dc2ebbc9a2a7fa2361cc_3e8caf1e = /*#__PURE__*/ (() => {
const Button_button_899cbce24fd6dc2ebbc9a2a7fa2361cc_3e8caf1e = memo(({children, ...rest}) => {
    const on_click_adc242d37c187bd0026fd1a6ada9816d = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.set_selected_rating", ({ ["value"] : "1" }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])



    return(
        jsx("button",{...mergeSlotProps(rest, ({ "aria-label":"Nota 1 de 5", className:"rating-star", onClick:on_click_adc242d37c187bd0026fd1a6ada9816d, type:"button" }))},children)
    )
});
Button_button_899cbce24fd6dc2ebbc9a2a7fa2361cc_3e8caf1e.displayName = "Button";
return Button_button_899cbce24fd6dc2ebbc9a2a7fa2361cc_3e8caf1e;
})();

export const Button_button_4b9178460cd34f79688e053ba3d109c2_3e8caf1e = /*#__PURE__*/ (() => {
const Button_button_4b9178460cd34f79688e053ba3d109c2_3e8caf1e = memo(({children, ...rest}) => {
    const on_click_befc5c44e812728540b1b3e54d8277a6 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.set_selected_rating", ({ ["value"] : "2" }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])



    return(
        jsx("button",{...mergeSlotProps(rest, ({ "aria-label":"Nota 2 de 5", className:"rating-star", onClick:on_click_befc5c44e812728540b1b3e54d8277a6, type:"button" }))},children)
    )
});
Button_button_4b9178460cd34f79688e053ba3d109c2_3e8caf1e.displayName = "Button";
return Button_button_4b9178460cd34f79688e053ba3d109c2_3e8caf1e;
})();

export const Button_button_9a875a5be1a5c5f65726ea850555cc5e_3e8caf1e = /*#__PURE__*/ (() => {
const Button_button_9a875a5be1a5c5f65726ea850555cc5e_3e8caf1e = memo(({children, ...rest}) => {
    const on_click_f6c9e21e8a3b9c223c6630c6082a379f = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.set_selected_rating", ({ ["value"] : "3" }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])



    return(
        jsx("button",{...mergeSlotProps(rest, ({ "aria-label":"Nota 3 de 5", className:"rating-star", onClick:on_click_f6c9e21e8a3b9c223c6630c6082a379f, type:"button" }))},children)
    )
});
Button_button_9a875a5be1a5c5f65726ea850555cc5e_3e8caf1e.displayName = "Button";
return Button_button_9a875a5be1a5c5f65726ea850555cc5e_3e8caf1e;
})();

export const Button_button_8491cc5487ad226f3fccdf0e666d2fd1_3e8caf1e = /*#__PURE__*/ (() => {
const Button_button_8491cc5487ad226f3fccdf0e666d2fd1_3e8caf1e = memo(({children, ...rest}) => {
    const on_click_c3f559b7f0addb6b77ddd44ba3a6363c = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.set_selected_rating", ({ ["value"] : "4" }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])



    return(
        jsx("button",{...mergeSlotProps(rest, ({ "aria-label":"Nota 4 de 5", className:"rating-star", onClick:on_click_c3f559b7f0addb6b77ddd44ba3a6363c, type:"button" }))},children)
    )
});
Button_button_8491cc5487ad226f3fccdf0e666d2fd1_3e8caf1e.displayName = "Button";
return Button_button_8491cc5487ad226f3fccdf0e666d2fd1_3e8caf1e;
})();

export const Button_button_7f41fd713f00473947e2d65e1c9f7826_3e8caf1e = /*#__PURE__*/ (() => {
const Button_button_7f41fd713f00473947e2d65e1c9f7826_3e8caf1e = memo(({children, ...rest}) => {
    const on_click_f7ba70710eb556b2bdb1686401631a57 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.set_selected_rating", ({ ["value"] : "5" }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])



    return(
        jsx("button",{...mergeSlotProps(rest, ({ "aria-label":"Nota 5 de 5", className:"rating-star", onClick:on_click_f7ba70710eb556b2bdb1686401631a57, type:"button" }))},children)
    )
});
Button_button_7f41fd713f00473947e2d65e1c9f7826_3e8caf1e.displayName = "Button";
return Button_button_7f41fd713f00473947e2d65e1c9f7826_3e8caf1e;
})();

export const Valuenumberinput_input_1e12611767324c80bbfa298410a33f68_3e8caf1e = /*#__PURE__*/ (() => {
const Valuenumberinput_input_1e12611767324c80bbfa298410a33f68_3e8caf1e = memo(({children, ...rest}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        jsx("input",{...mergeSlotProps(rest, ({ className:"w-full rounded-xl border border-white/15 bg-[#151719] px-4 py-3 text-white", defaultValue:reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.selected_rating_rx_state_, max:5, min:0, name:"rating", placeholder:"0 a 5", step:0.5, type:"number" }))},)
    )
});
Valuenumberinput_input_1e12611767324c80bbfa298410a33f68_3e8caf1e.displayName = "ValueNumberInput";
return Valuenumberinput_input_1e12611767324c80bbfa298410a33f68_3e8caf1e;
})();

export const Textarea_textarea_b19ab4a6cd15a517128414672fc2055e_3e8caf1e = /*#__PURE__*/ (() => {
const Textarea_textarea_b19ab4a6cd15a517128414672fc2055e_3e8caf1e = memo(({children, ...rest}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        jsx("textarea",{...mergeSlotProps(rest, ({ className:"w-full rounded-xl border border-white/15 bg-[#151719] px-4 py-3 text-white", defaultValue:reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.selected_review_rx_state_, maxLength:10000, name:"review", placeholder:"Conte o que achou desta obra...", rows:5 }))},)
    )
});
Textarea_textarea_b19ab4a6cd15a517128414672fc2055e_3e8caf1e.displayName = "Textarea";
return Textarea_textarea_b19ab4a6cd15a517128414672fc2055e_3e8caf1e;
})();

export const Checkboxinput_input_fa0132feed37da48b4d78b08428dd803_3e8caf1e = /*#__PURE__*/ (() => {
const Checkboxinput_input_fa0132feed37da48b4d78b08428dd803_3e8caf1e = memo(({children, ...rest}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        jsx("input",{...mergeSlotProps(rest, ({ defaultChecked:reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.selected_spoiler_rx_state_, name:"spoiler", type:"checkbox" }))},)
    )
});
Checkboxinput_input_fa0132feed37da48b4d78b08428dd803_3e8caf1e.displayName = "CheckboxInput";
return Checkboxinput_input_fa0132feed37da48b4d78b08428dd803_3e8caf1e;
})();

export const Form_form_c13ad414f299775b0843bf3609c4f3d2_3e8caf1e = /*#__PURE__*/ (() => {
const Form_form_c13ad414f299775b0843bf3609c4f3d2_3e8caf1e = memo(({children, ...rest}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)

    const handleSubmit_e21fb790279d1bd5a1dbca3af4a4e7c6 = useCallback((ev) => {
        const $form = ev.target
        ev.preventDefault()
        const form_data = {...Object.fromEntries(new FormData($form).entries()), ...({  })};

        (((...args) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.save_interaction", ({ ["form"] : form_data }), ({  })))], args, ({  }))))(ev));

        if (false) {
            $form.reset()
        }
    })
    


    return(
        jsx("form",{...mergeSlotProps(rest, ({ className:"media-review-form", key:((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.selected_rx_state_?.["id"]+reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.selected_review_rx_state_)+reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.selected_rating_rx_state_), onSubmit:handleSubmit_e21fb790279d1bd5a1dbca3af4a4e7c6 }))},children)
    )
});
Form_form_c13ad414f299775b0843bf3609c4f3d2_3e8caf1e.displayName = "Form";
return Form_form_c13ad414f299775b0843bf3609c4f3d2_3e8caf1e;
})();

export const Button_button_5124c14b3db2c6109a0629a0227f1d56_3e8caf1e = /*#__PURE__*/ (() => {
const Button_button_5124c14b3db2c6109a0629a0227f1d56_3e8caf1e = memo(({children, ...rest}) => {
    const on_click_9d96b913db1de3a5a81d29bba43d3f7e = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.quick_add", ({ ["status"] : "planned", ["rating"] : 0, ["list_title"] : "Quero ver / ler" }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])



    return(
        jsx("button",{...mergeSlotProps(rest, ({ className:"media-list-link", onClick:on_click_9d96b913db1de3a5a81d29bba43d3f7e }))},children)
    )
});
Button_button_5124c14b3db2c6109a0629a0227f1d56_3e8caf1e.displayName = "Button";
return Button_button_5124c14b3db2c6109a0629a0227f1d56_3e8caf1e;
})();

export const Button_button_c148cc9eda051075367142b943296dee_3e8caf1e = /*#__PURE__*/ (() => {
const Button_button_c148cc9eda051075367142b943296dee_3e8caf1e = memo(({children, ...rest}) => {
    const on_click_345153183042d95bf3d0ebcc946ea7fd = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.quick_add", ({ ["status"] : "completed", ["rating"] : 0, ["list_title"] : "J\u00e1 assisti / li" }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])



    return(
        jsx("button",{...mergeSlotProps(rest, ({ className:"media-list-link", onClick:on_click_345153183042d95bf3d0ebcc946ea7fd }))},children)
    )
});
Button_button_c148cc9eda051075367142b943296dee_3e8caf1e.displayName = "Button";
return Button_button_c148cc9eda051075367142b943296dee_3e8caf1e;
})();

export const Foreach_comp_846a126569b60dfae2f600dd7936cf27_3e8caf1e = /*#__PURE__*/ (() => {
const Foreach_comp_846a126569b60dfae2f600dd7936cf27_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        Array.prototype.map.call(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.community_reviews_rx_state_ ?? [],((review_rx_state_,index_ce020f59451bf7f0fe95666927b056c8)=>(jsx("article",{className:"media-community-review",key:index_ce020f59451bf7f0fe95666927b056c8},jsx("div",{className:"flex flex-wrap items-center gap-2"},jsx("strong",{},review_rx_state_?.["author"]),jsx(Fragment,{},(!((review_rx_state_?.["rating"]?.valueOf?.() === ""?.valueOf?.()))?(jsx(Fragment,{},jsx("span",{className:"brand-yellow"},("  \u00b7  Nota "+review_rx_state_?.["rating"])))):(jsx(Fragment,{},)))),jsx(Fragment,{},(!((review_rx_state_?.["date"]?.valueOf?.() === ""?.valueOf?.()))?(jsx(Fragment,{},jsx("span",{className:"text-xs text-gray-500"},("  \u00b7  "+review_rx_state_?.["date"])))):(jsx(Fragment,{},))))),jsx("p",{className:"text-sm leading-relaxed whitespace-pre-wrap mt-3"},review_rx_state_?.["body"])))))
    )
});
Foreach_comp_846a126569b60dfae2f600dd7936cf27_3e8caf1e.displayName = "Foreach";
return Foreach_comp_846a126569b60dfae2f600dd7936cf27_3e8caf1e;
})();

export const Cond_comp_963d878769abab51562d508ea8fb1bb5_3e8caf1e = /*#__PURE__*/ (() => {
const Cond_comp_963d878769abab51562d508ea8fb1bb5_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        ((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.community_reviews_rx_state_.length > 0)?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_963d878769abab51562d508ea8fb1bb5_3e8caf1e.displayName = "Cond";
return Cond_comp_963d878769abab51562d508ea8fb1bb5_3e8caf1e;
})();

export const Foreach_comp_6031cef70423231c16b0d667f96b112e_3e8caf1e = /*#__PURE__*/ (() => {
const Foreach_comp_6031cef70423231c16b0d667f96b112e_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        Array.prototype.map.call(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.recommendations_rx_state_ ?? [],((m_rx_state_,index_48297cae80c3860334ecd3c3b748b1e8)=>(jsx("button",{className:"media-card text-left",key:index_48297cae80c3860334ecd3c3b748b1e8,onClick:((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.open_recommendation", ({ ["source"] : m_rx_state_?.["source"], ["identifier"] : m_rx_state_?.["external_id"] }), ({  })))], [_e], ({  })))),type:"button"},jsx("div",{className:"cover-frame"},jsx("div",{"aria-hidden":true,className:"cover-placeholder"},jsx("span",{className:"cover-placeholder-brand"},"CODEBOXD"),jsx("div",{className:"cover-placeholder-copy"},jsx("span",{className:"cover-placeholder-label"},"Capa indispon\u00edvel"))),jsx(Fragment,{},(pyAnd(!((m_rx_state_?.["cover"]?.valueOf?.() === ""?.valueOf?.())), () => (!(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.failed_covers_rx_state_.includes(m_rx_state_?.["cover"]))))?(jsx(Fragment,{},jsx("img",{alt:m_rx_state_?.["title"],className:"media-cover",css:({ ["width"] : "100%", ["height"] : "100%" }),decoding:"async",loading:"lazy",onError:((...args) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.cover_failed", ({ ["url"] : m_rx_state_?.["cover"] }), ({  })))], args, ({  })))),src:m_rx_state_?.["cover"]},))):(jsx(Fragment,{},))))),jsx("div",{className:"p-4"},jsx("h3",{className:"font-semibold line-clamp-2"},m_rx_state_?.["title"]),jsx("p",{className:"text-sm text-gray-400"},m_rx_state_?.["year"]))))))
    )
});
Foreach_comp_6031cef70423231c16b0d667f96b112e_3e8caf1e.displayName = "Foreach";
return Foreach_comp_6031cef70423231c16b0d667f96b112e_3e8caf1e;
})();

export const Cond_comp_06f2fea709e1de8700708055a97e42a2_3e8caf1e = /*#__PURE__*/ (() => {
const Cond_comp_06f2fea709e1de8700708055a97e42a2_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        ((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.recommendations_rx_state_.length > 0)?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_06f2fea709e1de8700708055a97e42a2_3e8caf1e.displayName = "Cond";
return Cond_comp_06f2fea709e1de8700708055a97e42a2_3e8caf1e;
})();

export const Cond_comp_98dacd92cd460ea0370d5c4150cd569f_3e8caf1e = /*#__PURE__*/ (() => {
const Cond_comp_98dacd92cd460ea0370d5c4150cd569f_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        (!((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.selected_rx_state_?.["title"]?.valueOf?.() === ""?.valueOf?.()))?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_98dacd92cd460ea0370d5c4150cd569f_3e8caf1e.displayName = "Cond";
return Cond_comp_98dacd92cd460ea0370d5c4150cd569f_3e8caf1e;
})();

export const Foreach_comp_1e9af9a296083ef18e38a2d8ba2bc6ae_3e8caf1e = /*#__PURE__*/ (() => {
const Foreach_comp_1e9af9a296083ef18e38a2d8ba2bc6ae_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        Array.prototype.map.call(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.visible_library_rx_state_ ?? [],((i_rx_state_,index_2ef475f95355dadd562ead256c35aaf4)=>(jsx("article",{className:"activity-card",key:index_2ef475f95355dadd562ead256c35aaf4},jsx(ReactRouterLink,{className:"activity-cover",to:("/obra/"+i_rx_state_?.["id"])},jsx(Fragment,{},(!((i_rx_state_?.["cover"]?.valueOf?.() === ""?.valueOf?.()))?(jsx(Fragment,{},jsx("img",{alt:i_rx_state_?.["title"],loading:"lazy",src:i_rx_state_?.["cover"]},))):(jsx(Fragment,{},jsx(LucideBookOpen,{size:28},)))))),jsx("div",{className:"min-w-0"},jsx(ReactRouterLink,{className:"font-semibold",to:("/obra/"+i_rx_state_?.["id"])},i_rx_state_?.["title"]),jsx("p",{className:"activity-meta"},((((i_rx_state_?.["kind"]+" \u00b7 ")+i_rx_state_?.["status"])+" \u00b7 ")+i_rx_state_?.["rating"])),jsx(Fragment,{},((i_rx_state_?.["spoiler"]?.valueOf?.() === "True"?.valueOf?.())?(jsx(Fragment,{},jsx("details",{},jsx("summary",{className:"cursor-pointer text-amber-300"},"Mostrar conte\u00fado com spoilers"),jsx("p",{className:"whitespace-pre-wrap mt-3"},i_rx_state_?.["review"])))):(jsx(Fragment,{},jsx("p",{className:"whitespace-pre-wrap"},i_rx_state_?.["review"]))))))))))
    )
});
Foreach_comp_1e9af9a296083ef18e38a2d8ba2bc6ae_3e8caf1e.displayName = "Foreach";
return Foreach_comp_1e9af9a296083ef18e38a2d8ba2bc6ae_3e8caf1e;
})();

export const Cond_comp_20f69ae950a32360ae9751f5ba69d177_3e8caf1e = /*#__PURE__*/ (() => {
const Cond_comp_20f69ae950a32360ae9751f5ba69d177_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        ((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.library_rx_state_.length > 0)?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_20f69ae950a32360ae9751f5ba69d177_3e8caf1e.displayName = "Cond";
return Cond_comp_20f69ae950a32360ae9751f5ba69d177_3e8caf1e;
})();

export const Button_button_90648db7273547a24d47e43a764e1acf_3e8caf1e = /*#__PURE__*/ (() => {
const Button_button_90648db7273547a24d47e43a764e1acf_3e8caf1e = memo(({children, ...rest}) => {
    const on_click_9efc09e834df01cf738ce33703737286 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.show_more", ({  }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])



    return(
        jsx("button",{...mergeSlotProps(rest, ({ className:"action-button", onClick:on_click_9efc09e834df01cf738ce33703737286, type:"button" }))},children)
    )
});
Button_button_90648db7273547a24d47e43a764e1acf_3e8caf1e.displayName = "Button";
return Button_button_90648db7273547a24d47e43a764e1acf_3e8caf1e;
})();

export const Cond_comp_1747b7e5a09132ea33abcbbc7f3de705_3e8caf1e = /*#__PURE__*/ (() => {
const Cond_comp_1747b7e5a09132ea33abcbbc7f3de705_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        ((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.library_rx_state_.length > reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.visible_count_rx_state_)?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_1747b7e5a09132ea33abcbbc7f3de705_3e8caf1e.displayName = "Cond";
return Cond_comp_1747b7e5a09132ea33abcbbc7f3de705_3e8caf1e;
})();

export const Foreach_comp_7bb80b9ef31f1ef27a28d11a419c4493_3e8caf1e = /*#__PURE__*/ (() => {
const Foreach_comp_7bb80b9ef31f1ef27a28d11a419c4493_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)
const reflex___state____state__codeboxd_main___state___session____session_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state)



    return(
        Array.prototype.map.call(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.visible_people_rx_state_ ?? [],((p_rx_state_,index_e0d187db7a257ea520f63a3a836a1e66)=>(jsx("article",{className:"rounded-2xl border border-white/10 bg-[#111114] p-5 space-y-4",key:index_e0d187db7a257ea520f63a3a836a1e66},jsx(ReactRouterLink,{className:"text-xl font-semibold",to:("/perfil/"+p_rx_state_?.["user_id"])},p_rx_state_?.["display_name"]),jsx("p",{className:"text-[#F5B300]"},("@"+p_rx_state_?.["username"])),jsx("p",{className:"text-gray-400"},p_rx_state_?.["bio"]),jsx(Fragment,{},(pyAnd(reflex___state____state__codeboxd_main___state___session____session_state.is_authenticated_rx_state_, () => (!((p_rx_state_?.["user_id"]?.valueOf?.() === (JSON.stringify(reflex___state____state__codeboxd_main___state___session____session_state.user_id_rx_state_))?.valueOf?.()))))?(jsx(Fragment,{},jsx("button",{className:"action-button",onClick:((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.follow", ({ ["uid"] : p_rx_state_?.["user_id"] }), ({  })))], [_e], ({  })))),type:"button"},(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.following_ids_rx_state_.includes(p_rx_state_?.["user_id"]) ? "Deixar de seguir" : "Seguir")))):(jsx(Fragment,{},))))))))
    )
});
Foreach_comp_7bb80b9ef31f1ef27a28d11a419c4493_3e8caf1e.displayName = "Foreach";
return Foreach_comp_7bb80b9ef31f1ef27a28d11a419c4493_3e8caf1e;
})();

export const Cond_comp_45d1c18b459c580d8d7fa3d915ffd2b7_3e8caf1e = /*#__PURE__*/ (() => {
const Cond_comp_45d1c18b459c580d8d7fa3d915ffd2b7_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        ((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.visible_people_rx_state_.length > 0)?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_45d1c18b459c580d8d7fa3d915ffd2b7_3e8caf1e.displayName = "Cond";
return Cond_comp_45d1c18b459c580d8d7fa3d915ffd2b7_3e8caf1e;
})();

export const Cond_comp_48d69d677e69fb61acb4a1b6f343340f_3e8caf1e = /*#__PURE__*/ (() => {
const Cond_comp_48d69d677e69fb61acb4a1b6f343340f_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        ((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.people_rx_state_.length > reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.visible_count_rx_state_)?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_48d69d677e69fb61acb4a1b6f343340f_3e8caf1e.displayName = "Cond";
return Cond_comp_48d69d677e69fb61acb4a1b6f343340f_3e8caf1e;
})();

export const Bare_comp_5f0d93664368d908299e25e297a82e75_3e8caf1e = /*#__PURE__*/ (() => {
const Bare_comp_5f0d93664368d908299e25e297a82e75_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        (!((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.edit_post_id_rx_state_?.valueOf?.() === ""?.valueOf?.())) ? "Editar publica\u00e7\u00e3o" : "Criar publica\u00e7\u00e3o")
    )
});
Bare_comp_5f0d93664368d908299e25e297a82e75_3e8caf1e.displayName = "Bare";
return Bare_comp_5f0d93664368d908299e25e297a82e75_3e8caf1e;
})();

export const Input_input_3d7dc3f512083bf3112fefdade1750ba_3e8caf1e = /*#__PURE__*/ (() => {
const Input_input_3d7dc3f512083bf3112fefdade1750ba_3e8caf1e = memo(({children, ...rest}) => {
    const on_change_36bd4ee87662fb80ee062da768bdd4f1 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.update_post_media_query", ({ ["value"] : _e?.["target"]?.["value"] }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])
const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        jsx("input",{...mergeSlotProps(rest, ({ className:"w-full rounded-xl border border-white/15 bg-[#151719] px-4 py-3 text-white", onChange:on_change_36bd4ee87662fb80ee062da768bdd4f1, placeholder:"Pesquisar filme, serie, anime ou livro", type:"search", value:(isNotNullOrUndefined(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.post_media_query_rx_state_) ? reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.post_media_query_rx_state_ : "") }))},)
    )
});
Input_input_3d7dc3f512083bf3112fefdade1750ba_3e8caf1e.displayName = "Input";
return Input_input_3d7dc3f512083bf3112fefdade1750ba_3e8caf1e;
})();

export const Bare_comp_0d863a0014acc0971ad3982ff64bab9d_3e8caf1e = /*#__PURE__*/ (() => {
const Bare_comp_0d863a0014acc0971ad3982ff64bab9d_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        (reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.post_media_searching_rx_state_ ? "Pesquisando..." : "Pesquisar obra")
    )
});
Bare_comp_0d863a0014acc0971ad3982ff64bab9d_3e8caf1e.displayName = "Bare";
return Bare_comp_0d863a0014acc0971ad3982ff64bab9d_3e8caf1e;
})();

export const Button_button_b46b4fec2b7958b2f80c77f3a6f80309_3e8caf1e = /*#__PURE__*/ (() => {
const Button_button_b46b4fec2b7958b2f80c77f3a6f80309_3e8caf1e = memo(({children, ...rest}) => {
    const on_click_69e437f7f41afc88d6f5c4e09893b4d1 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.search_post_media", ({  }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])



    return(
        jsx("button",{...mergeSlotProps(rest, ({ className:"action-button", onClick:on_click_69e437f7f41afc88d6f5c4e09893b4d1, type:"button" }))},children)
    )
});
Button_button_b46b4fec2b7958b2f80c77f3a6f80309_3e8caf1e.displayName = "Button";
return Button_button_b46b4fec2b7958b2f80c77f3a6f80309_3e8caf1e;
})();

export const Img_img_2b3eb99d3b09b7b464c482e52b93666d_3e8caf1e = /*#__PURE__*/ (() => {
const Img_img_2b3eb99d3b09b7b464c482e52b93666d_3e8caf1e = memo(({children, ...rest}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        jsx("img",{...mergeSlotProps(rest, ({ alt:reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.post_media_selected_rx_state_?.["title"], className:"post-media-selected-cover", src:reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.post_media_selected_rx_state_?.["cover"] }))},)
    )
});
Img_img_2b3eb99d3b09b7b464c482e52b93666d_3e8caf1e.displayName = "Img";
return Img_img_2b3eb99d3b09b7b464c482e52b93666d_3e8caf1e;
})();

export const Cond_comp_d4a4f3f47986b0040ef96f32c17dd3b0_3e8caf1e = /*#__PURE__*/ (() => {
const Cond_comp_d4a4f3f47986b0040ef96f32c17dd3b0_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        (!((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.post_media_selected_rx_state_?.["cover"]?.valueOf?.() === ""?.valueOf?.()))?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_d4a4f3f47986b0040ef96f32c17dd3b0_3e8caf1e.displayName = "Cond";
return Cond_comp_d4a4f3f47986b0040ef96f32c17dd3b0_3e8caf1e;
})();

export const Bare_comp_c03c927999fbf55aab2055b851fdcf22_3e8caf1e = /*#__PURE__*/ (() => {
const Bare_comp_c03c927999fbf55aab2055b851fdcf22_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.post_media_selected_rx_state_?.["title"]
    )
});
Bare_comp_c03c927999fbf55aab2055b851fdcf22_3e8caf1e.displayName = "Bare";
return Bare_comp_c03c927999fbf55aab2055b851fdcf22_3e8caf1e;
})();

export const Button_button_e5f254044debe91435512b4107fb5147_3e8caf1e = /*#__PURE__*/ (() => {
const Button_button_e5f254044debe91435512b4107fb5147_3e8caf1e = memo(({children, ...rest}) => {
    const on_click_cd37c59f1b5e64c99007a0b773824cfa = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.clear_post_media", ({  }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])



    return(
        jsx("button",{...mergeSlotProps(rest, ({ className:"action-button", onClick:on_click_cd37c59f1b5e64c99007a0b773824cfa, type:"button" }))},children)
    )
});
Button_button_e5f254044debe91435512b4107fb5147_3e8caf1e.displayName = "Button";
return Button_button_e5f254044debe91435512b4107fb5147_3e8caf1e;
})();

export const Cond_comp_b1896b16ace92880399bf13553f2d1d7_3e8caf1e = /*#__PURE__*/ (() => {
const Cond_comp_b1896b16ace92880399bf13553f2d1d7_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        (!((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.post_media_selected_rx_state_?.["id"]?.valueOf?.() === ""?.valueOf?.()))?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_b1896b16ace92880399bf13553f2d1d7_3e8caf1e.displayName = "Cond";
return Cond_comp_b1896b16ace92880399bf13553f2d1d7_3e8caf1e;
})();

export const Foreach_comp_9d5fc98bbd25f4137eac54e8ca42215f_3e8caf1e = /*#__PURE__*/ (() => {
const Foreach_comp_9d5fc98bbd25f4137eac54e8ca42215f_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        Array.prototype.map.call(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.post_media_results_rx_state_ ?? [],((item_rx_state_,index_a167cb1e441218a9a40a938d4d81713f)=>(jsx("button",{className:"post-media-result",key:index_a167cb1e441218a9a40a938d4d81713f,onClick:((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.select_post_media", ({ ["key"] : item_rx_state_?.["key"] }), ({  })))], [_e], ({  })))),type:"button"},jsx(Fragment,{},(!((item_rx_state_?.["cover"]?.valueOf?.() === ""?.valueOf?.()))?(jsx(Fragment,{},jsx("img",{alt:"",className:"post-media-result-cover",src:item_rx_state_?.["cover"]},))):(jsx(Fragment,{},jsx(LucideClapperboard,{size:22},))))),jsx("span",{className:"font-semibold"},item_rx_state_?.["title"]),jsx("span",{className:"text-xs text-gray-400"},((item_rx_state_?.["kind"]+" \u00b7 ")+item_rx_state_?.["year"]))))))
    )
});
Foreach_comp_9d5fc98bbd25f4137eac54e8ca42215f_3e8caf1e.displayName = "Foreach";
return Foreach_comp_9d5fc98bbd25f4137eac54e8ca42215f_3e8caf1e;
})();

export const Cond_comp_1b84220ff793475a5bdebbb5241fb5a7_3e8caf1e = /*#__PURE__*/ (() => {
const Cond_comp_1b84220ff793475a5bdebbb5241fb5a7_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        ((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.post_media_results_rx_state_.length > 0)?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_1b84220ff793475a5bdebbb5241fb5a7_3e8caf1e.displayName = "Cond";
return Cond_comp_1b84220ff793475a5bdebbb5241fb5a7_3e8caf1e;
})();

export const Cond_comp_9410a27a8fed449ccb8da5dad2c0bcc1_3e8caf1e = /*#__PURE__*/ (() => {
const Cond_comp_9410a27a8fed449ccb8da5dad2c0bcc1_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        (reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.post_media_searching_rx_state_?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_9410a27a8fed449ccb8da5dad2c0bcc1_3e8caf1e.displayName = "Cond";
return Cond_comp_9410a27a8fed449ccb8da5dad2c0bcc1_3e8caf1e;
})();

export const Styledupload_comp_02b33644726191ec05822d24b88f869e_3e8caf1e = /*#__PURE__*/ (() => {
const Styledupload_comp_02b33644726191ec05822d24b88f869e_3e8caf1e = memo(({children}) => {
    const ref_post_image_upload = useRef(null); refs["ref_post_image_upload"] = ref_post_image_upload;
const [filesById, setFilesById] = useContext(UploadFilesContext);
const on_drop_9f1deeb86bc3599517b16d1ee2c8d7b3 = useCallback(((_ev_0) => ((e => setFilesById(filesById => {
    const updatedFilesById = Object.assign({}, filesById);
    updatedFilesById["post_image_upload"] = e;
    return updatedFilesById;
  })
    )(_ev_0))), [addEvents, ReflexEvent, filesById, setFilesById])
const on_drop_rejected_bedc1fe7e7d4fcbcbc646af9fb7688c4 = useCallback(((_ev_0) => (addEvents([(ReflexEvent("_call_function", ({ ["function"] : (() => (refs['__toast']?.["error"]("", ({ ["title"] : "Files not Accepted", ["description"] : _ev_0.map(((pmuoeieh) => (pmuoeieh?.["file"]?.["path"]+": "+pmuoeieh?.["errors"].map(((xrrixsns) => xrrixsns?.["message"])).join(", ")))).join("\n\n"), ["closeButton"] : true, ["style"] : ({ ["whiteSpace"] : "pre-line" }) })))), ["callback"] : null }), ({  })))], [_ev_0], ({  })))), [addEvents, ReflexEvent])
const { getRootProps: miuwrhvk, getInputProps: tufrxhfo, isDragActive: yybhbzkm} = useDropzone(({ ["accept"] : ({ ["image/png"] : [".png"], ["image/jpeg"] : [".jpg", ".jpeg"], ["image/webp"] : [".webp"], ["image/gif"] : [".gif"] }), ["maxFiles"] : 1, ["maxSize"] : 5242880, ["multiple"] : true, ["id"] : "post_image_upload", ["onDrop"] : on_drop_9f1deeb86bc3599517b16d1ee2c8d7b3, ["onDropRejected"] : on_drop_rejected_bedc1fe7e7d4fcbcbc646af9fb7688c4 }));



    return(
        jsx(Fragment,{},jsx("div",{className:"rx-Upload post-image-dropzone",css:({ ["border"] : "1px dashed var(--accent-12)", ["padding"] : "5em", ["textAlign"] : "center" }),id:"post_image_upload",ref:ref_post_image_upload,...miuwrhvk()},jsx("input",{type:"file",...tufrxhfo()},),jsx("div",{className:"post-image-upload-prompt"},jsx(LucideImageUp,{size:22},),jsx("span",{className:"text-sm"},"Escolha ou arraste uma imagem (ate 5 MB)"))))
    )
});
Styledupload_comp_02b33644726191ec05822d24b88f869e_3e8caf1e.displayName = "StyledUpload";
return Styledupload_comp_02b33644726191ec05822d24b88f869e_3e8caf1e;
})();

export const Bare_comp_e865fb6f9caf83db4f63f502dd1296b1_3e8caf1e = /*#__PURE__*/ (() => {
const Bare_comp_e865fb6f9caf83db4f63f502dd1296b1_3e8caf1e = memo(({children}) => {
    const [filesById, setFilesById] = useContext(UploadFilesContext);



    return(
        (filesById["post_image_upload"] ? filesById["post_image_upload"].map((f) => f.name) : [])?.at?.(0)
    )
});
Bare_comp_e865fb6f9caf83db4f63f502dd1296b1_3e8caf1e.displayName = "Bare";
return Bare_comp_e865fb6f9caf83db4f63f502dd1296b1_3e8caf1e;
})();

export const Button_button_48080dbe15f56f5fe550f315453f8903_3e8caf1e = /*#__PURE__*/ (() => {
const Button_button_48080dbe15f56f5fe550f315453f8903_3e8caf1e = memo(({children, ...rest}) => {
    const [filesById, setFilesById] = useContext(UploadFilesContext);
const on_click_2c3ba9fadeccd7196edb54699494f273 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.stage_post_image", ({ ["files"] : filesById?.["post_image_upload"], ["upload_param_name"] : "files", ["upload_id"] : "post_image_upload", ["extra_headers"] : ({  }) }), ({  }), "uploadFiles"))], [_e], ({  })))), [addEvents, ReflexEvent, filesById, setFilesById])



    return(
        jsx("button",{...mergeSlotProps(rest, ({ className:"action-button", onClick:on_click_2c3ba9fadeccd7196edb54699494f273, type:"button" }))},children)
    )
});
Button_button_48080dbe15f56f5fe550f315453f8903_3e8caf1e.displayName = "Button";
return Button_button_48080dbe15f56f5fe550f315453f8903_3e8caf1e;
})();

export const Cond_comp_b8c556058993b093eafc3547e199a467_3e8caf1e = /*#__PURE__*/ (() => {
const Cond_comp_b8c556058993b093eafc3547e199a467_3e8caf1e = memo(({children}) => {
    const [filesById, setFilesById] = useContext(UploadFilesContext);



    return(
        (((filesById["post_image_upload"] ? filesById["post_image_upload"].map((f) => f.name) : []).length > 0)?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_b8c556058993b093eafc3547e199a467_3e8caf1e.displayName = "Cond";
return Cond_comp_b8c556058993b093eafc3547e199a467_3e8caf1e;
})();

export const Img_img_a814a3a6ec328e3cbe895a1049847d87_3e8caf1e = /*#__PURE__*/ (() => {
const Img_img_a814a3a6ec328e3cbe895a1049847d87_3e8caf1e = memo(({children, ...rest}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        jsx("img",{...mergeSlotProps(rest, ({ alt:"Previa da imagem enviada", className:"post-image-preview", src:(getBackendURL(env.UPLOAD)+"/"+reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.post_image_filename_rx_state_) }))},)
    )
});
Img_img_a814a3a6ec328e3cbe895a1049847d87_3e8caf1e.displayName = "Img";
return Img_img_a814a3a6ec328e3cbe895a1049847d87_3e8caf1e;
})();

export const Button_button_ee25226f2a714102308e4c73a9afdb33_3e8caf1e = /*#__PURE__*/ (() => {
const Button_button_ee25226f2a714102308e4c73a9afdb33_3e8caf1e = memo(({children, ...rest}) => {
    const on_click_a8d1605ed6b97a09112897d4cec16d7d = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.remove_post_image", ({  }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])



    return(
        jsx("button",{...mergeSlotProps(rest, ({ className:"action-button", onClick:on_click_a8d1605ed6b97a09112897d4cec16d7d, type:"button" }))},children)
    )
});
Button_button_ee25226f2a714102308e4c73a9afdb33_3e8caf1e.displayName = "Button";
return Button_button_ee25226f2a714102308e4c73a9afdb33_3e8caf1e;
})();

export const Img_img_bb42397fd3e29e1cc8a2e676b18ef1de_3e8caf1e = /*#__PURE__*/ (() => {
const Img_img_bb42397fd3e29e1cc8a2e676b18ef1de_3e8caf1e = memo(({children, ...rest}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        jsx("img",{...mergeSlotProps(rest, ({ alt:"Imagem atual da publicacao", className:"post-image-preview", src:reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.post_existing_image_url_rx_state_ }))},)
    )
});
Img_img_bb42397fd3e29e1cc8a2e676b18ef1de_3e8caf1e.displayName = "Img";
return Img_img_bb42397fd3e29e1cc8a2e676b18ef1de_3e8caf1e;
})();

export const Cond_comp_43cac89d52968054ce1f94e75ad23fca_3e8caf1e = /*#__PURE__*/ (() => {
const Cond_comp_43cac89d52968054ce1f94e75ad23fca_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        (!((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.post_existing_image_url_rx_state_?.valueOf?.() === ""?.valueOf?.()))?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_43cac89d52968054ce1f94e75ad23fca_3e8caf1e.displayName = "Cond";
return Cond_comp_43cac89d52968054ce1f94e75ad23fca_3e8caf1e;
})();

export const Cond_comp_a740a40f50bcd3f296dabd15e333cbd6_3e8caf1e = /*#__PURE__*/ (() => {
const Cond_comp_a740a40f50bcd3f296dabd15e333cbd6_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        (!((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.post_image_filename_rx_state_?.valueOf?.() === ""?.valueOf?.()))?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_a740a40f50bcd3f296dabd15e333cbd6_3e8caf1e.displayName = "Cond";
return Cond_comp_a740a40f50bcd3f296dabd15e333cbd6_3e8caf1e;
})();

export const Textarea_textarea_9a826ee7372a72be59c4b6a9fe51b70c_3e8caf1e = /*#__PURE__*/ (() => {
const Textarea_textarea_9a826ee7372a72be59c4b6a9fe51b70c_3e8caf1e = memo(({children, ...rest}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        jsx("textarea",{...mergeSlotProps(rest, ({ className:"w-full rounded-xl border border-white/15 bg-[#151719] px-4 py-3 text-white", defaultValue:reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.edit_post_body_rx_state_, maxLength:5000, name:"body", required:true }))},)
    )
});
Textarea_textarea_9a826ee7372a72be59c4b6a9fe51b70c_3e8caf1e.displayName = "Textarea";
return Textarea_textarea_9a826ee7372a72be59c4b6a9fe51b70c_3e8caf1e;
})();

export const Checkboxinput_input_2baa3660dba9add680dd354803bde87e_3e8caf1e = /*#__PURE__*/ (() => {
const Checkboxinput_input_2baa3660dba9add680dd354803bde87e_3e8caf1e = memo(({children, ...rest}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        jsx("input",{...mergeSlotProps(rest, ({ defaultChecked:reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.edit_post_spoiler_rx_state_, name:"spoiler", type:"checkbox" }))},)
    )
});
Checkboxinput_input_2baa3660dba9add680dd354803bde87e_3e8caf1e.displayName = "CheckboxInput";
return Checkboxinput_input_2baa3660dba9add680dd354803bde87e_3e8caf1e;
})();

export const Bare_comp_20fa286ab22292d935fafdf4a6faba4d_3e8caf1e = /*#__PURE__*/ (() => {
const Bare_comp_20fa286ab22292d935fafdf4a6faba4d_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        (!((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.edit_post_id_rx_state_?.valueOf?.() === ""?.valueOf?.())) ? "Salvar edi\u00e7\u00e3o" : "Publicar")
    )
});
Bare_comp_20fa286ab22292d935fafdf4a6faba4d_3e8caf1e.displayName = "Bare";
return Bare_comp_20fa286ab22292d935fafdf4a6faba4d_3e8caf1e;
})();

export const Form_form_058615582562b7af0fe3387980ecf087_3e8caf1e = /*#__PURE__*/ (() => {
const Form_form_058615582562b7af0fe3387980ecf087_3e8caf1e = memo(({children, ...rest}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)

    const handleSubmit_e88da5267d6c8efdf753c061f86ccd03 = useCallback((ev) => {
        const $form = ev.target
        ev.preventDefault()
        const form_data = {...Object.fromEntries(new FormData($form).entries()), ...({  })};

        (((...args) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.save_post", ({ ["form"] : form_data }), ({  })))], args, ({  }))))(ev));

        if (false) {
            $form.reset()
        }
    })
    


    return(
        jsx("form",{...mergeSlotProps(rest, ({ className:"editor-form", key:reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.edit_post_id_rx_state_, onSubmit:handleSubmit_e88da5267d6c8efdf753c061f86ccd03 }))},children)
    )
});
Form_form_058615582562b7af0fe3387980ecf087_3e8caf1e.displayName = "Form";
return Form_form_058615582562b7af0fe3387980ecf087_3e8caf1e;
})();

export const Dialogroot_dialog__root_6d848b35a90d8d5d38fb8143acf253ec_3e8caf1e = /*#__PURE__*/ (() => {
const Dialogroot_dialog__root_6d848b35a90d8d5d38fb8143acf253ec_3e8caf1e = memo(({children, ...rest}) => {
    const on_open_change_41982dc794bba4a11020357952e82780 = useCallback(((_ev_0) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.set_post_editor_open", ({ ["value"] : _ev_0 }), ({  })))], [_ev_0], ({  })))), [addEvents, ReflexEvent])
const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        jsx(RadixThemesDialog.Root,{...mergeSlotProps(rest, ({ onOpenChange:on_open_change_41982dc794bba4a11020357952e82780, open:reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.post_editor_open_rx_state_ }))},children)
    )
});
Dialogroot_dialog__root_6d848b35a90d8d5d38fb8143acf253ec_3e8caf1e.displayName = "DialogRoot";
return Dialogroot_dialog__root_6d848b35a90d8d5d38fb8143acf253ec_3e8caf1e;
})();

export const Foreach_comp_97cdf18ad9a489024168ef363bbc9dc4_3e8caf1e = /*#__PURE__*/ (() => {
const Foreach_comp_97cdf18ad9a489024168ef363bbc9dc4_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)
const reflex___state____state__codeboxd_main___state___session____session_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state)



    return(
        Array.prototype.map.call(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.visible_posts_rx_state_ ?? [],((p_rx_state_,index_df033d50f0e9edc23b1e9a8779432019)=>(jsx("article",{className:"post-card",key:index_df033d50f0e9edc23b1e9a8779432019},jsx("div",{className:"post-author"},jsx(ReactRouterLink,{to:("/perfil/"+p_rx_state_?.["user_id"])},jsx(Fragment,{},(!((p_rx_state_?.["avatar"]?.valueOf?.() === ""?.valueOf?.()))?(jsx(Fragment,{},jsx("img",{alt:p_rx_state_?.["author"],className:"avatar",src:p_rx_state_?.["avatar"]},))):(jsx(Fragment,{},jsx("span",{className:"avatar avatar-fallback"},jsx(LucideUserRound,{size:22},))))))),jsx("div",{},jsx(ReactRouterLink,{className:"font-semibold",to:("/perfil/"+p_rx_state_?.["user_id"])},p_rx_state_?.["author"]),jsx("p",{className:"text-xs text-gray-500"},p_rx_state_?.["published_at"]))),jsx(Fragment,{},(!((p_rx_state_?.["media_cover"]?.valueOf?.() === ""?.valueOf?.()))?(jsx(Fragment,{},jsx(ReactRouterLink,{to:("/obra/"+p_rx_state_?.["media_id"])},jsx("img",{alt:p_rx_state_?.["media_title"],className:"post-cover",loading:"lazy",src:p_rx_state_?.["media_cover"]},)))):(jsx(Fragment,{},)))),jsx(Fragment,{},(!((p_rx_state_?.["media_id"]?.valueOf?.() === "0"?.valueOf?.()))?(jsx(Fragment,{},jsx(ReactRouterLink,{className:"block brand-yellow",to:("/obra/"+p_rx_state_?.["media_id"])},p_rx_state_?.["media_title"]))):(jsx(Fragment,{},)))),jsx(Fragment,{},(!((p_rx_state_?.["image_url"]?.valueOf?.() === ""?.valueOf?.()))?(jsx(Fragment,{},jsx("img",{alt:"Imagem anexada a publicacao",className:"w-full max-h-[600px] rounded-2xl object-contain bg-[#171714]",loading:"lazy",src:p_rx_state_?.["image_url"]},))):(jsx(Fragment,{},)))),jsx(Fragment,{},((p_rx_state_?.["spoiler"]?.valueOf?.() === "True"?.valueOf?.())?(jsx(Fragment,{},jsx("details",{},jsx("summary",{className:"cursor-pointer text-amber-300"},"Mostrar conte\u00fado com spoilers"),jsx("p",{className:"whitespace-pre-wrap mt-3"},p_rx_state_?.["body"])))):(jsx(Fragment,{},jsx("p",{className:"whitespace-pre-wrap"},p_rx_state_?.["body"]))))),jsx("div",{className:"post-actions"},jsx("button",{className:"quiet-button",onClick:((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.like", ({ ["pid"] : p_rx_state_?.["id"] }), ({  })))], [_e], ({  }))))},jsx(LucideHeart,{size:18},),(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.liked_posts_rx_state_.includes(p_rx_state_?.["id"]) ? "Descurtir" : "Curtir")),jsx("button",{className:"quiet-button",onClick:((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.discussion", ({ ["pid"] : p_rx_state_?.["id"] }), ({  })))], [_e], ({  }))))},jsx(LucideMessageCircle,{size:18},),(!((p_rx_state_?.["comments_count"]?.valueOf?.() === ""?.valueOf?.())) ? (p_rx_state_?.["comments_count"]+" coment\u00e1rios") : "Coment\u00e1rios")),jsx(Fragment,{},(!((p_rx_state_?.["likes_count"]?.valueOf?.() === ""?.valueOf?.()))?(jsx(Fragment,{},jsx("span",{className:"text-sm text-gray-400"},(p_rx_state_?.["likes_count"]+" curtidas")))):(jsx(Fragment,{},)))),jsx(Fragment,{},(!((p_rx_state_?.["user_id"]?.valueOf?.() === (JSON.stringify(reflex___state____state__codeboxd_main___state___session____session_state.user_id_rx_state_))?.valueOf?.()))?(jsx(Fragment,{},jsx("button",{className:"quiet-button",onClick:((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.open_report", ({ ["target_type"] : "post", ["target_id"] : p_rx_state_?.["id"] }), ({  })))], [_e], ({  }))))},"Denunciar"))):(jsx(Fragment,{},)))),jsx(Fragment,{},((p_rx_state_?.["user_id"]?.valueOf?.() === (JSON.stringify(reflex___state____state__codeboxd_main___state___session____session_state.user_id_rx_state_))?.valueOf?.())?(jsx(Fragment,{},jsx("button",{className:"quiet-button",onClick:((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.edit_post", ({ ["pid"] : p_rx_state_?.["id"] }), ({  })))], [_e], ({  }))))},"Editar"),jsx(RadixThemesAlertDialog.Root,{},jsx(RadixThemesAlertDialog.Trigger,{},jsx("button",{className:"quiet-button danger",type:"button"},"Excluir publica\u00e7\u00e3o")),jsx(RadixThemesAlertDialog.Content,{className:"codeboxd-dialog confirm-dialog"},jsx(RadixThemesAlertDialog.Title,{},"Excluir publica\u00e7\u00e3o?"),jsx(RadixThemesAlertDialog.Description,{},"Esta a\u00e7\u00e3o remove o conte\u00fado. Deseja continuar?"),jsx(RadixThemesFlex,{className:"confirm-dialog-actions",css:({ ["gap"] : "3", ["marginTop"] : "20px" }),justify:"end"},jsx(RadixThemesAlertDialog.Cancel,{},jsx(RadixThemesButton,{className:"confirm-cancel-button",variant:"soft"},"Cancelar")),jsx(RadixThemesAlertDialog.Action,{},jsx(RadixThemesFlex,{},jsx(RadixThemesButton,{color:"red",onClick:((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.remove_post", ({ ["pid"] : p_rx_state_?.["id"] }), ({  })))], [_e], ({  }))))},"Confirmar exclus\u00e3o")))))))):(jsx(Fragment,{},)))))))))
    )
});
Foreach_comp_97cdf18ad9a489024168ef363bbc9dc4_3e8caf1e.displayName = "Foreach";
return Foreach_comp_97cdf18ad9a489024168ef363bbc9dc4_3e8caf1e;
})();

export const Cond_comp_c4394415e04edc5d4bee1908782120ee_3e8caf1e = /*#__PURE__*/ (() => {
const Cond_comp_c4394415e04edc5d4bee1908782120ee_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        ((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.posts_rx_state_.length > 0)?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_c4394415e04edc5d4bee1908782120ee_3e8caf1e.displayName = "Cond";
return Cond_comp_c4394415e04edc5d4bee1908782120ee_3e8caf1e;
})();

export const Cond_comp_ed452d3771e0307aedb1aac2b8ba36e5_3e8caf1e = /*#__PURE__*/ (() => {
const Cond_comp_ed452d3771e0307aedb1aac2b8ba36e5_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        ((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.posts_rx_state_.length > reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.visible_count_rx_state_)?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_ed452d3771e0307aedb1aac2b8ba36e5_3e8caf1e.displayName = "Cond";
return Cond_comp_ed452d3771e0307aedb1aac2b8ba36e5_3e8caf1e;
})();

export const Button_button_ee85a27db2cf73bfbebc580c773c7b74_3e8caf1e = /*#__PURE__*/ (() => {
const Button_button_ee85a27db2cf73bfbebc580c773c7b74_3e8caf1e = memo(({children, ...rest}) => {
    const on_click_8221dc93568f0bc2a5a036556ba69910 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.close_discussion", ({  }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])



    return(
        jsx("button",{...mergeSlotProps(rest, ({ className:"action-button", onClick:on_click_8221dc93568f0bc2a5a036556ba69910, type:"button" }))},children)
    )
});
Button_button_ee85a27db2cf73bfbebc580c773c7b74_3e8caf1e.displayName = "Button";
return Button_button_ee85a27db2cf73bfbebc580c773c7b74_3e8caf1e;
})();

export const Foreach_comp_913589881d14aa65d6e4906944b1a5e4_3e8caf1e = /*#__PURE__*/ (() => {
const Foreach_comp_913589881d14aa65d6e4906944b1a5e4_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)
const reflex___state____state__codeboxd_main___state___session____session_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state)



    return(
        Array.prototype.map.call(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.comments_rx_state_ ?? [],((c_rx_state_,index_9d07bd8954a06ac83a55af37346df964)=>(jsx("article",{className:"rounded-2xl border border-white/10 bg-[#111114] p-5 space-y-4",key:index_9d07bd8954a06ac83a55af37346df964},jsx(ReactRouterLink,{className:"font-semibold",to:("/perfil/"+c_rx_state_?.["user_id"])},c_rx_state_?.["author"]),jsx("p",{className:"whitespace-pre-wrap"},c_rx_state_?.["body"]),jsx(Fragment,{},((c_rx_state_?.["user_id"]?.valueOf?.() === (JSON.stringify(reflex___state____state__codeboxd_main___state___session____session_state.user_id_rx_state_))?.valueOf?.())?(jsx(Fragment,{},jsx("div",{className:"flex gap-3"},jsx("button",{className:"action-button",onClick:((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.edit_comment", ({ ["cid"] : c_rx_state_?.["id"] }), ({  })))], [_e], ({  })))),type:"button"},"Editar"),jsx(RadixThemesAlertDialog.Root,{},jsx(RadixThemesAlertDialog.Trigger,{},jsx("button",{className:"quiet-button danger",type:"button"},"Excluir coment\u00e1rio")),jsx(RadixThemesAlertDialog.Content,{className:"codeboxd-dialog confirm-dialog"},jsx(RadixThemesAlertDialog.Title,{},"Excluir coment\u00e1rio?"),jsx(RadixThemesAlertDialog.Description,{},"Esta a\u00e7\u00e3o remove o conte\u00fado. Deseja continuar?"),jsx(RadixThemesFlex,{className:"confirm-dialog-actions",css:({ ["gap"] : "3", ["marginTop"] : "20px" }),justify:"end"},jsx(RadixThemesAlertDialog.Cancel,{},jsx(RadixThemesButton,{className:"confirm-cancel-button",variant:"soft"},"Cancelar")),jsx(RadixThemesAlertDialog.Action,{},jsx(RadixThemesFlex,{},jsx(RadixThemesButton,{color:"red",onClick:((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.remove_comment", ({ ["cid"] : c_rx_state_?.["id"] }), ({  })))], [_e], ({  }))))},"Confirmar exclus\u00e3o"))))))))):(jsx(Fragment,{},jsx("button",{className:"quiet-button",onClick:((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.open_report", ({ ["target_type"] : "comment", ["target_id"] : c_rx_state_?.["id"] }), ({  })))], [_e], ({  }))))},"Denunciar")))))))))
    )
});
Foreach_comp_913589881d14aa65d6e4906944b1a5e4_3e8caf1e.displayName = "Foreach";
return Foreach_comp_913589881d14aa65d6e4906944b1a5e4_3e8caf1e;
})();

export const Cond_comp_8fdd6d9e67d9016cfc128dafebee2704_3e8caf1e = /*#__PURE__*/ (() => {
const Cond_comp_8fdd6d9e67d9016cfc128dafebee2704_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        ((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.comments_rx_state_.length > 0)?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_8fdd6d9e67d9016cfc128dafebee2704_3e8caf1e.displayName = "Cond";
return Cond_comp_8fdd6d9e67d9016cfc128dafebee2704_3e8caf1e;
})();

export const Textarea_textarea_76ccfd91de83ffd96b9ee9ba1027f341_3e8caf1e = /*#__PURE__*/ (() => {
const Textarea_textarea_76ccfd91de83ffd96b9ee9ba1027f341_3e8caf1e = memo(({children, ...rest}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        jsx("textarea",{...mergeSlotProps(rest, ({ className:"w-full rounded-xl border border-white/15 bg-[#151719] px-4 py-3 text-white", defaultValue:reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.edit_comment_body_rx_state_, maxLength:2000, name:"body", required:true }))},)
    )
});
Textarea_textarea_76ccfd91de83ffd96b9ee9ba1027f341_3e8caf1e.displayName = "Textarea";
return Textarea_textarea_76ccfd91de83ffd96b9ee9ba1027f341_3e8caf1e;
})();

export const Bare_comp_a5671a75638f2472c14765b8f71bdb0f_3e8caf1e = /*#__PURE__*/ (() => {
const Bare_comp_a5671a75638f2472c14765b8f71bdb0f_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        (!((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.edit_comment_id_rx_state_?.valueOf?.() === ""?.valueOf?.())) ? "Salvar edi\u00e7\u00e3o" : "Comentar")
    )
});
Bare_comp_a5671a75638f2472c14765b8f71bdb0f_3e8caf1e.displayName = "Bare";
return Bare_comp_a5671a75638f2472c14765b8f71bdb0f_3e8caf1e;
})();

export const Form_form_5d357cb8def77e9206638c4cd7a12dc6_3e8caf1e = /*#__PURE__*/ (() => {
const Form_form_5d357cb8def77e9206638c4cd7a12dc6_3e8caf1e = memo(({children, ...rest}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)

    const handleSubmit_ac13c8df08b00be58112a1a354a905a1 = useCallback((ev) => {
        const $form = ev.target
        ev.preventDefault()
        const form_data = {...Object.fromEntries(new FormData($form).entries()), ...({  })};

        (((...args) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.save_comment", ({ ["form"] : form_data }), ({  })))], args, ({  }))))(ev));

        if (false) {
            $form.reset()
        }
    })
    


    return(
        jsx("form",{...mergeSlotProps(rest, ({ className:"rounded-2xl border border-white/10 bg-[#111114] p-5 space-y-4", key:(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.selected_post_rx_state_+reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.edit_comment_id_rx_state_), onSubmit:handleSubmit_ac13c8df08b00be58112a1a354a905a1 }))},children)
    )
});
Form_form_5d357cb8def77e9206638c4cd7a12dc6_3e8caf1e.displayName = "Form";
return Form_form_5d357cb8def77e9206638c4cd7a12dc6_3e8caf1e;
})();

export const Cond_comp_2c71f76f754cecfaf24830c6e6a8291a_3e8caf1e = /*#__PURE__*/ (() => {
const Cond_comp_2c71f76f754cecfaf24830c6e6a8291a_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        (!((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.selected_post_rx_state_?.valueOf?.() === ""?.valueOf?.()))?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_2c71f76f754cecfaf24830c6e6a8291a_3e8caf1e.displayName = "Cond";
return Cond_comp_2c71f76f754cecfaf24830c6e6a8291a_3e8caf1e;
})();

export const Button_button_0c35431fc6f123b3dab2222f699b6d87_3e8caf1e = /*#__PURE__*/ (() => {
const Button_button_0c35431fc6f123b3dab2222f699b6d87_3e8caf1e = memo(({children, ...rest}) => {
    const on_click_5513d5b7c38dfbe621da7ee3e02d8fcb = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.new_post", ({  }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])



    return(
        jsx("button",{...mergeSlotProps(rest, ({ className:"action-button", onClick:on_click_5513d5b7c38dfbe621da7ee3e02d8fcb, type:"button" }))},children)
    )
});
Button_button_0c35431fc6f123b3dab2222f699b6d87_3e8caf1e.displayName = "Button";
return Button_button_0c35431fc6f123b3dab2222f699b6d87_3e8caf1e;
})();

export const Foreach_comp_42f07d99a844a53b10e8df5a8b092e17_3e8caf1e = /*#__PURE__*/ (() => {
const Foreach_comp_42f07d99a844a53b10e8df5a8b092e17_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        Array.prototype.map.call(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.suggested_people_rx_state_ ?? [],((p_rx_state_,index_8903120a65660c30e8d2e584b1fd0126)=>(jsx(ReactRouterLink,{className:"sidebar-person",key:index_8903120a65660c30e8d2e584b1fd0126,to:("/perfil/"+p_rx_state_?.["user_id"])},jsx(Fragment,{},(!((p_rx_state_?.["avatar_url"]?.valueOf?.() === ""?.valueOf?.()))?(jsx(Fragment,{},jsx("img",{alt:p_rx_state_?.["display_name"],className:"avatar",src:p_rx_state_?.["avatar_url"]},))):(jsx(Fragment,{},jsx("span",{className:"avatar avatar-fallback"},jsx(LucideUserRound,{size:22},)))))),jsx("div",{},jsx("strong",{},p_rx_state_?.["display_name"]),jsx("p",{},("@"+p_rx_state_?.["username"])))))))
    )
});
Foreach_comp_42f07d99a844a53b10e8df5a8b092e17_3e8caf1e.displayName = "Foreach";
return Foreach_comp_42f07d99a844a53b10e8df5a8b092e17_3e8caf1e;
})();

export const Button_button_7a871d2058af49aff0186433ecbcf5df_3e8caf1e = /*#__PURE__*/ (() => {
const Button_button_7a871d2058af49aff0186433ecbcf5df_3e8caf1e = memo(({children, ...rest}) => {
    const on_click_71af9dfb457562c8e1287528fc04ef54 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.new_list", ({  }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])



    return(
        jsx("button",{...mergeSlotProps(rest, ({ className:"action-button", onClick:on_click_71af9dfb457562c8e1287528fc04ef54, type:"button" }))},children)
    )
});
Button_button_7a871d2058af49aff0186433ecbcf5df_3e8caf1e.displayName = "Button";
return Button_button_7a871d2058af49aff0186433ecbcf5df_3e8caf1e;
})();

export const Bare_comp_1b1b6da33535e28af0910c17e8a6cc35_3e8caf1e = /*#__PURE__*/ (() => {
const Bare_comp_1b1b6da33535e28af0910c17e8a6cc35_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        ((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.selected_list_rx_state_?.["id"]?.valueOf?.() === ""?.valueOf?.()) ? "Criar lista" : "Editar lista")
    )
});
Bare_comp_1b1b6da33535e28af0910c17e8a6cc35_3e8caf1e.displayName = "Bare";
return Bare_comp_1b1b6da33535e28af0910c17e8a6cc35_3e8caf1e;
})();

export const Input_input_1ca1babcf0b6a35e22546ab413d89371_3e8caf1e = /*#__PURE__*/ (() => {
const Input_input_1ca1babcf0b6a35e22546ab413d89371_3e8caf1e = memo(({children, ...rest}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        jsx("input",{...mergeSlotProps(rest, ({ className:"w-full rounded-xl border border-white/15 bg-[#151719] px-4 py-3 text-white", defaultValue:reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.selected_list_rx_state_?.["title"], maxLength:120, name:"title", required:true }))},)
    )
});
Input_input_1ca1babcf0b6a35e22546ab413d89371_3e8caf1e.displayName = "Input";
return Input_input_1ca1babcf0b6a35e22546ab413d89371_3e8caf1e;
})();

export const Textarea_textarea_322e037ebcfd7a177c895189b615c2bf_3e8caf1e = /*#__PURE__*/ (() => {
const Textarea_textarea_322e037ebcfd7a177c895189b615c2bf_3e8caf1e = memo(({children, ...rest}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        jsx("textarea",{...mergeSlotProps(rest, ({ className:"w-full rounded-xl border border-white/15 bg-[#151719] px-4 py-3 text-white", defaultValue:reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.selected_list_rx_state_?.["description"], maxLength:2000, name:"description" }))},)
    )
});
Textarea_textarea_322e037ebcfd7a177c895189b615c2bf_3e8caf1e.displayName = "Textarea";
return Textarea_textarea_322e037ebcfd7a177c895189b615c2bf_3e8caf1e;
})();

export const Checkboxinput_input_6f392901ab5eb684ac4f262c5248a4d8_3e8caf1e = /*#__PURE__*/ (() => {
const Checkboxinput_input_6f392901ab5eb684ac4f262c5248a4d8_3e8caf1e = memo(({children, ...rest}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        jsx("input",{...mergeSlotProps(rest, ({ defaultChecked:(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.selected_list_rx_state_?.["is_public"]?.valueOf?.() === "True"?.valueOf?.()), name:"is_public", type:"checkbox" }))},)
    )
});
Checkboxinput_input_6f392901ab5eb684ac4f262c5248a4d8_3e8caf1e.displayName = "CheckboxInput";
return Checkboxinput_input_6f392901ab5eb684ac4f262c5248a4d8_3e8caf1e;
})();

export const Form_form_08d0b879973da11443efc2104855e98c_3e8caf1e = /*#__PURE__*/ (() => {
const Form_form_08d0b879973da11443efc2104855e98c_3e8caf1e = memo(({children, ...rest}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)

    const handleSubmit_2a5472ad7a59e7b752cd46f630a1e1aa = useCallback((ev) => {
        const $form = ev.target
        ev.preventDefault()
        const form_data = {...Object.fromEntries(new FormData($form).entries()), ...({  })};

        (((...args) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.save_list", ({ ["form"] : form_data }), ({  })))], args, ({  }))))(ev));

        if (false) {
            $form.reset()
        }
    })
    


    return(
        jsx("form",{...mergeSlotProps(rest, ({ className:"editor-form", key:(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.selected_list_rx_state_?.["id"]+reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.selected_list_rx_state_?.["title"]), onSubmit:handleSubmit_2a5472ad7a59e7b752cd46f630a1e1aa }))},children)
    )
});
Form_form_08d0b879973da11443efc2104855e98c_3e8caf1e.displayName = "Form";
return Form_form_08d0b879973da11443efc2104855e98c_3e8caf1e;
})();

export const Dialogroot_dialog__root_c5638c44bee28955510a934d9d2b4819_3e8caf1e = /*#__PURE__*/ (() => {
const Dialogroot_dialog__root_c5638c44bee28955510a934d9d2b4819_3e8caf1e = memo(({children, ...rest}) => {
    const on_open_change_4e0c9a0544c5cf5d3a8a741a2c0299c5 = useCallback(((_ev_0) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.set_list_editor_open", ({ ["value"] : _ev_0 }), ({  })))], [_ev_0], ({  })))), [addEvents, ReflexEvent])
const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        jsx(RadixThemesDialog.Root,{...mergeSlotProps(rest, ({ onOpenChange:on_open_change_4e0c9a0544c5cf5d3a8a741a2c0299c5, open:reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.list_editor_open_rx_state_ }))},children)
    )
});
Dialogroot_dialog__root_c5638c44bee28955510a934d9d2b4819_3e8caf1e.displayName = "DialogRoot";
return Dialogroot_dialog__root_c5638c44bee28955510a934d9d2b4819_3e8caf1e;
})();

export const Foreach_comp_98e66443e58a3a34e038ffadfcc10741_3e8caf1e = /*#__PURE__*/ (() => {
const Foreach_comp_98e66443e58a3a34e038ffadfcc10741_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        Array.prototype.map.call(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.visible_lists_rx_state_ ?? [],((item_rx_state_,index_04c5cc45af6886ae00d907bfbaa45289)=>(jsx("button",{className:"list-row",key:index_04c5cc45af6886ae00d907bfbaa45289,onClick:((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.open_list", ({ ["lid"] : item_rx_state_?.["id"] }), ({  })))], [_e], ({  })))),type:"button"},jsx(LucideListVideo,{size:20},),jsx("span",{},item_rx_state_?.["title"]),jsx("span",{className:"list-visibility"},((item_rx_state_?.["is_public"]?.valueOf?.() === "True"?.valueOf?.()) ? "P\u00fablica" : "Privada")),jsx(LucideChevronRight,{size:18},)))))
    )
});
Foreach_comp_98e66443e58a3a34e038ffadfcc10741_3e8caf1e.displayName = "Foreach";
return Foreach_comp_98e66443e58a3a34e038ffadfcc10741_3e8caf1e;
})();

export const Cond_comp_5930c108b61e0ba66390e6e3a7ec01da_3e8caf1e = /*#__PURE__*/ (() => {
const Cond_comp_5930c108b61e0ba66390e6e3a7ec01da_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        ((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.lists_rx_state_.length > 0)?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_5930c108b61e0ba66390e6e3a7ec01da_3e8caf1e.displayName = "Cond";
return Cond_comp_5930c108b61e0ba66390e6e3a7ec01da_3e8caf1e;
})();

export const Cond_comp_bc383160ef8710d31db1dbc1bd942311_3e8caf1e = /*#__PURE__*/ (() => {
const Cond_comp_bc383160ef8710d31db1dbc1bd942311_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        ((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.lists_rx_state_.length > reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.visible_count_rx_state_)?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_bc383160ef8710d31db1dbc1bd942311_3e8caf1e.displayName = "Cond";
return Cond_comp_bc383160ef8710d31db1dbc1bd942311_3e8caf1e;
})();

export const Bare_comp_bcd21d5b0372b55ad172cf9db1961651_3e8caf1e = /*#__PURE__*/ (() => {
const Bare_comp_bcd21d5b0372b55ad172cf9db1961651_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.selected_list_rx_state_?.["title"]
    )
});
Bare_comp_bcd21d5b0372b55ad172cf9db1961651_3e8caf1e.displayName = "Bare";
return Bare_comp_bcd21d5b0372b55ad172cf9db1961651_3e8caf1e;
})();

export const Bare_comp_47cd4345b0ef2c6f1bab654ddcdde036_3e8caf1e = /*#__PURE__*/ (() => {
const Bare_comp_47cd4345b0ef2c6f1bab654ddcdde036_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.selected_list_rx_state_?.["description"]
    )
});
Bare_comp_47cd4345b0ef2c6f1bab654ddcdde036_3e8caf1e.displayName = "Bare";
return Bare_comp_47cd4345b0ef2c6f1bab654ddcdde036_3e8caf1e;
})();

export const Button_button_b383a9bf49949c107478ee497f263756_3e8caf1e = /*#__PURE__*/ (() => {
const Button_button_b383a9bf49949c107478ee497f263756_3e8caf1e = memo(({children, ...rest}) => {
    const on_click_8e026e7f771610b08ef7090dd5b3ff63 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.set_list_editor_open", ({ ["value"] : true }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])



    return(
        jsx("button",{...mergeSlotProps(rest, ({ className:"action-button", onClick:on_click_8e026e7f771610b08ef7090dd5b3ff63, type:"button" }))},children)
    )
});
Button_button_b383a9bf49949c107478ee497f263756_3e8caf1e.displayName = "Button";
return Button_button_b383a9bf49949c107478ee497f263756_3e8caf1e;
})();

export const Button_button_6b41484d4e481427457c6b958c331463_3e8caf1e = /*#__PURE__*/ (() => {
const Button_button_6b41484d4e481427457c6b958c331463_3e8caf1e = memo(({children, ...rest}) => {
    const on_click_628f0773fb680d34f1479c6c23c94c23 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.remove_list", ({  }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])



    return(
        jsx(RadixThemesButton,{...mergeSlotProps(rest, ({ color:"red", onClick:on_click_628f0773fb680d34f1479c6c23c94c23 }))},children)
    )
});
Button_button_6b41484d4e481427457c6b958c331463_3e8caf1e.displayName = "Button";
return Button_button_6b41484d4e481427457c6b958c331463_3e8caf1e;
})();

export const Cond_comp_86741388a4afe84bf86b6b4ad2446217_3e8caf1e = /*#__PURE__*/ (() => {
const Cond_comp_86741388a4afe84bf86b6b4ad2446217_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        (reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.owns_list_rx_state_?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_86741388a4afe84bf86b6b4ad2446217_3e8caf1e.displayName = "Cond";
return Cond_comp_86741388a4afe84bf86b6b4ad2446217_3e8caf1e;
})();

export const Foreach_comp_4fed9be5cc5293070e77c3ca96908a76_3e8caf1e = /*#__PURE__*/ (() => {
const Foreach_comp_4fed9be5cc5293070e77c3ca96908a76_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        Array.prototype.map.call(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.catalog_items_rx_state_ ?? [],((m_rx_state_,index_09b52d5f3a7764254e630e744628a8fd)=>(jsx("option",{key:index_09b52d5f3a7764254e630e744628a8fd,value:m_rx_state_?.["id"]},m_rx_state_?.["title"]))))
    )
});
Foreach_comp_4fed9be5cc5293070e77c3ca96908a76_3e8caf1e.displayName = "Foreach";
return Foreach_comp_4fed9be5cc5293070e77c3ca96908a76_3e8caf1e;
})();

export const Form_form_672c5e586cb4f18fc0612e70f4aa1056_3e8caf1e = /*#__PURE__*/ (() => {
const Form_form_672c5e586cb4f18fc0612e70f4aa1056_3e8caf1e = memo(({children, ...rest}) => {
    

    const handleSubmit_eeb52a6fd96adeb1374e919444ab9fe3 = useCallback((ev) => {
        const $form = ev.target
        ev.preventDefault()
        const form_data = {...Object.fromEntries(new FormData($form).entries()), ...({  })};

        (((...args) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.add_list_item", ({ ["form"] : form_data }), ({  })))], args, ({  }))))(ev));

        if (false) {
            $form.reset()
        }
    })
    


    return(
        jsx("form",{...mergeSlotProps(rest, ({ className:"list-add-form", onSubmit:handleSubmit_eeb52a6fd96adeb1374e919444ab9fe3 }))},children)
    )
});
Form_form_672c5e586cb4f18fc0612e70f4aa1056_3e8caf1e.displayName = "Form";
return Form_form_672c5e586cb4f18fc0612e70f4aa1056_3e8caf1e;
})();

export const Foreach_comp_90ddaec3403761ac96f4affec8e3ba42_3e8caf1e = /*#__PURE__*/ (() => {
const Foreach_comp_90ddaec3403761ac96f4affec8e3ba42_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        Array.prototype.map.call(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.list_items_rx_state_ ?? [],((m_rx_state_,index_276a47e828911b072ab0e242aeff5aa3)=>(jsx("article",{className:"list-media-item",key:index_276a47e828911b072ab0e242aeff5aa3},jsx(ReactRouterLink,{className:"media-card",to:("/obra/"+m_rx_state_?.["id"])},jsx("div",{className:"h-full"},jsx("div",{className:"cover-frame"},jsx("div",{"aria-hidden":true,className:"cover-placeholder"},jsx("span",{className:"cover-placeholder-brand"},"CODEBOXD"),jsx("div",{className:"cover-placeholder-copy"},jsx("span",{className:"cover-placeholder-label"},"Capa indispon\u00edvel"))),jsx(Fragment,{},(pyAnd(!((m_rx_state_?.["cover"]?.valueOf?.() === ""?.valueOf?.())), () => (!(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.failed_covers_rx_state_.includes(m_rx_state_?.["cover"]))))?(jsx(Fragment,{},jsx("img",{alt:m_rx_state_?.["title"],className:"media-cover",css:({ ["width"] : "100%", ["height"] : "100%" }),decoding:"async",loading:"lazy",onError:((...args) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.cover_failed", ({ ["url"] : m_rx_state_?.["cover"] }), ({  })))], args, ({  })))),src:m_rx_state_?.["cover"]},))):(jsx(Fragment,{},))))),jsx("div",{className:"p-4"},jsx("h3",{className:"font-semibold line-clamp-2"},m_rx_state_?.["title"]),jsx("p",{className:"text-sm text-gray-400 mt-3"},((m_rx_state_?.["kind"]+" \u00b7 ")+m_rx_state_?.["year"]))))),jsx(Fragment,{},(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.owns_list_rx_state_?(jsx(Fragment,{},jsx(RadixThemesAlertDialog.Root,{},jsx(RadixThemesAlertDialog.Trigger,{},jsx("button",{className:"quiet-button danger",type:"button"},"Remover obra")),jsx(RadixThemesAlertDialog.Content,{className:"codeboxd-dialog confirm-dialog"},jsx(RadixThemesAlertDialog.Title,{},"Remover obra?"),jsx(RadixThemesAlertDialog.Description,{},"Esta a\u00e7\u00e3o remove o conte\u00fado. Deseja continuar?"),jsx(RadixThemesFlex,{className:"confirm-dialog-actions",css:({ ["gap"] : "3", ["marginTop"] : "20px" }),justify:"end"},jsx(RadixThemesAlertDialog.Cancel,{},jsx(RadixThemesButton,{className:"confirm-cancel-button",variant:"soft"},"Cancelar")),jsx(RadixThemesAlertDialog.Action,{},jsx(RadixThemesFlex,{},jsx(RadixThemesButton,{color:"red",onClick:((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___social____social_state.remove_list_item", ({ ["mid"] : m_rx_state_?.["id"] }), ({  })))], [_e], ({  }))))},"Confirmar exclus\u00e3o")))))))):(jsx(Fragment,{},))))))))
    )
});
Foreach_comp_90ddaec3403761ac96f4affec8e3ba42_3e8caf1e.displayName = "Foreach";
return Foreach_comp_90ddaec3403761ac96f4affec8e3ba42_3e8caf1e;
})();

export const Cond_comp_f4736c580542e5021b53cfb7be43f306_3e8caf1e = /*#__PURE__*/ (() => {
const Cond_comp_f4736c580542e5021b53cfb7be43f306_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        ((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.list_items_rx_state_.length > 0)?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_f4736c580542e5021b53cfb7be43f306_3e8caf1e.displayName = "Cond";
return Cond_comp_f4736c580542e5021b53cfb7be43f306_3e8caf1e;
})();

export const Cond_comp_8b5a12c9d7ec1010a95b366e20bde114_3e8caf1e = /*#__PURE__*/ (() => {
const Cond_comp_8b5a12c9d7ec1010a95b366e20bde114_3e8caf1e = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state)



    return(
        (!((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___social____social_state.selected_list_rx_state_?.["id"]?.valueOf?.() === ""?.valueOf?.()))?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_8b5a12c9d7ec1010a95b366e20bde114_3e8caf1e.displayName = "Cond";
return Cond_comp_8b5a12c9d7ec1010a95b366e20bde114_3e8caf1e;
})();
