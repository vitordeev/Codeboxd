
import {ReflexEvent,applyEventActions,getRefValue,getRefValues,isNotNullOrUndefined,isTrue,mergeSlotProps,refs} from "$/utils/state"
import {StateContexts,addEvents} from "$/utils/context"
import {Fragment,memo,useCallback,useContext,useEffect,useRef} from "react"
import {jsx} from "@emotion/react"
import LucideMessageSquareText from "lucide-react/dist/esm/icons/message-square-text.mjs"
import LucideClapperboard from "lucide-react/dist/esm/icons/clapperboard.mjs"








export const Button_button_812bd98f23a88229e0770231fd2c7a8b_b2269bd1 = /*#__PURE__*/ (() => {
const Button_button_812bd98f23a88229e0770231fd2c7a8b_b2269bd1 = memo(({children, ...rest}) => {
    const on_click_04fd11fb12f6e03482bf1190dac1510d = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.logout", ({  }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])



    return(
        jsx("button",{...mergeSlotProps(rest, ({ className:"quiet-button admin-logout-button", onClick:on_click_04fd11fb12f6e03482bf1190dac1510d, type:"button" }))},children)
    )
});
Button_button_812bd98f23a88229e0770231fd2c7a8b_b2269bd1.displayName = "Button";
return Button_button_812bd98f23a88229e0770231fd2c7a8b_b2269bd1;
})();

export const Bare_comp_7331c1fb6daa93c390cf1e237e6c72bf_b2269bd1 = /*#__PURE__*/ (() => {
const Bare_comp_7331c1fb6daa93c390cf1e237e6c72bf_b2269bd1 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        ("Atualizado em "+reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.dashboard_updated_at_rx_state_)
    )
});
Bare_comp_7331c1fb6daa93c390cf1e237e6c72bf_b2269bd1.displayName = "Bare";
return Bare_comp_7331c1fb6daa93c390cf1e237e6c72bf_b2269bd1;
})();

export const Cond_comp_3c92e83ee53b7fde9b0ce15034796c3d_b2269bd1 = /*#__PURE__*/ (() => {
const Cond_comp_3c92e83ee53b7fde9b0ce15034796c3d_b2269bd1 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        (!((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.dashboard_updated_at_rx_state_?.valueOf?.() === ""?.valueOf?.()))?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_3c92e83ee53b7fde9b0ce15034796c3d_b2269bd1.displayName = "Cond";
return Cond_comp_3c92e83ee53b7fde9b0ce15034796c3d_b2269bd1;
})();

export const Bare_comp_5168d80bb468c9860c3a1717e2b2dd11_b2269bd1 = /*#__PURE__*/ (() => {
const Bare_comp_5168d80bb468c9860c3a1717e2b2dd11_b2269bd1 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        (reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.dashboard_loading_rx_state_ ? "Atualizando\u2026" : "Atualizar")
    )
});
Bare_comp_5168d80bb468c9860c3a1717e2b2dd11_b2269bd1.displayName = "Bare";
return Bare_comp_5168d80bb468c9860c3a1717e2b2dd11_b2269bd1;
})();

export const Button_button_372d63f8875a036dcd35672a2205ef22_b2269bd1 = /*#__PURE__*/ (() => {
const Button_button_372d63f8875a036dcd35672a2205ef22_b2269bd1 = memo(({children, ...rest}) => {
    const on_click_4360fdbadb815f1833c2d70aa17fd402 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___admin____admin_state.load_dashboard", ({  }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])
const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        jsx("button",{...mergeSlotProps(rest, ({ className:"quiet-button admin-refresh-button", disabled:reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.dashboard_loading_rx_state_, onClick:on_click_4360fdbadb815f1833c2d70aa17fd402, type:"button" }))},children)
    )
});
Button_button_372d63f8875a036dcd35672a2205ef22_b2269bd1.displayName = "Button";
return Button_button_372d63f8875a036dcd35672a2205ef22_b2269bd1;
})();

export const Bare_comp_5ffa20dfca91cc92e5e6fcea275a029b_b2269bd1 = /*#__PURE__*/ (() => {
const Bare_comp_5ffa20dfca91cc92e5e6fcea275a029b_b2269bd1 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.dashboard_error_rx_state_
    )
});
Bare_comp_5ffa20dfca91cc92e5e6fcea275a029b_b2269bd1.displayName = "Bare";
return Bare_comp_5ffa20dfca91cc92e5e6fcea275a029b_b2269bd1;
})();

export const Cond_comp_c20d9eb1c21ca3cdf15166c14f783b6d_b2269bd1 = /*#__PURE__*/ (() => {
const Cond_comp_c20d9eb1c21ca3cdf15166c14f783b6d_b2269bd1 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        (!((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.dashboard_error_rx_state_?.valueOf?.() === ""?.valueOf?.()))?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_c20d9eb1c21ca3cdf15166c14f783b6d_b2269bd1.displayName = "Cond";
return Cond_comp_c20d9eb1c21ca3cdf15166c14f783b6d_b2269bd1;
})();

export const Cond_comp_3092b30034d68f1c7a37ce778a5c76cc_b2269bd1 = /*#__PURE__*/ (() => {
const Cond_comp_3092b30034d68f1c7a37ce778a5c76cc_b2269bd1 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        (reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.dashboard_loading_rx_state_?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_3092b30034d68f1c7a37ce778a5c76cc_b2269bd1.displayName = "Cond";
return Cond_comp_3092b30034d68f1c7a37ce778a5c76cc_b2269bd1;
})();

export const Bare_comp_7b9b55e265f1d308552fb70f7b8ac4cf_b2269bd1 = /*#__PURE__*/ (() => {
const Bare_comp_7b9b55e265f1d308552fb70f7b8ac4cf_b2269bd1 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.dashboard_stats_rx_state_?.["users_total"]
    )
});
Bare_comp_7b9b55e265f1d308552fb70f7b8ac4cf_b2269bd1.displayName = "Bare";
return Bare_comp_7b9b55e265f1d308552fb70f7b8ac4cf_b2269bd1;
})();

export const Bare_comp_72648945faaa6238216f9bed15867e28_b2269bd1 = /*#__PURE__*/ (() => {
const Bare_comp_72648945faaa6238216f9bed15867e28_b2269bd1 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.dashboard_stats_rx_state_?.["posts_total"]
    )
});
Bare_comp_72648945faaa6238216f9bed15867e28_b2269bd1.displayName = "Bare";
return Bare_comp_72648945faaa6238216f9bed15867e28_b2269bd1;
})();

export const Bare_comp_43bb6ce061048698cb543fd92c404a6e_b2269bd1 = /*#__PURE__*/ (() => {
const Bare_comp_43bb6ce061048698cb543fd92c404a6e_b2269bd1 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.dashboard_stats_rx_state_?.["media_total"]
    )
});
Bare_comp_43bb6ce061048698cb543fd92c404a6e_b2269bd1.displayName = "Bare";
return Bare_comp_43bb6ce061048698cb543fd92c404a6e_b2269bd1;
})();

export const Bare_comp_79879b575ce21ee0a70b48d067b2354d_b2269bd1 = /*#__PURE__*/ (() => {
const Bare_comp_79879b575ce21ee0a70b48d067b2354d_b2269bd1 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.dashboard_stats_rx_state_?.["reports_pending"]
    )
});
Bare_comp_79879b575ce21ee0a70b48d067b2354d_b2269bd1.displayName = "Bare";
return Bare_comp_79879b575ce21ee0a70b48d067b2354d_b2269bd1;
})();

export const Foreach_comp_b49a36d67c29ad4dfb9dd045263cef0d_b2269bd1 = /*#__PURE__*/ (() => {
const Foreach_comp_b49a36d67c29ad4dfb9dd045263cef0d_b2269bd1 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        Array.prototype.map.call(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.pending_reports_rx_state_ ?? [],((item_rx_state_,index_6f9b3bc31d545d61a9f0a0367d9f67d7)=>(jsx("li",{className:"admin-activity-item",key:index_6f9b3bc31d545d61a9f0a0367d9f67d7},jsx("div",{className:"admin-activity-row"},jsx("p",{className:"admin-activity-title"},((("Report #"+item_rx_state_?.["id"])+" \u00b7 ")+item_rx_state_?.["target_type"])),jsx("p",{className:"admin-activity-detail"},("Motivo: "+item_rx_state_?.["reason"])),jsx("time",{className:"admin-activity-time"},item_rx_state_?.["created_at"]))))))
    )
});
Foreach_comp_b49a36d67c29ad4dfb9dd045263cef0d_b2269bd1.displayName = "Foreach";
return Foreach_comp_b49a36d67c29ad4dfb9dd045263cef0d_b2269bd1;
})();

export const Cond_comp_cd1a77fd0bff6d2f2f916a498f0d1af6_b2269bd1 = /*#__PURE__*/ (() => {
const Cond_comp_cd1a77fd0bff6d2f2f916a498f0d1af6_b2269bd1 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        ((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.pending_reports_rx_state_.length > 0)?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_cd1a77fd0bff6d2f2f916a498f0d1af6_b2269bd1.displayName = "Cond";
return Cond_comp_cd1a77fd0bff6d2f2f916a498f0d1af6_b2269bd1;
})();

export const Foreach_comp_06510457e76be548018f6084eda4d24c_b2269bd1 = /*#__PURE__*/ (() => {
const Foreach_comp_06510457e76be548018f6084eda4d24c_b2269bd1 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        Array.prototype.map.call(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.recent_posts_rx_state_ ?? [],((item_rx_state_,index_5eb38dd2921f569461dcfa010d4bfd39)=>(jsx("li",{className:"admin-activity-item",key:index_5eb38dd2921f569461dcfa010d4bfd39},jsx("div",{className:"admin-activity-row"},jsx("div",{className:"admin-activity-icon"},jsx(LucideMessageSquareText,{size:18},)),jsx("div",{},jsx("p",{className:"admin-activity-title"},("Publica\u00e7\u00e3o #"+item_rx_state_?.["id"])),jsx("p",{className:"admin-activity-detail"},("Usu\u00e1rio #"+item_rx_state_?.["user_id"]))),jsx("time",{className:"admin-activity-time"},item_rx_state_?.["created_at"]))))))
    )
});
Foreach_comp_06510457e76be548018f6084eda4d24c_b2269bd1.displayName = "Foreach";
return Foreach_comp_06510457e76be548018f6084eda4d24c_b2269bd1;
})();

export const Cond_comp_930416ad1b5c3e4f65a5727c0b104d54_b2269bd1 = /*#__PURE__*/ (() => {
const Cond_comp_930416ad1b5c3e4f65a5727c0b104d54_b2269bd1 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        ((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.recent_posts_rx_state_.length > 0)?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_930416ad1b5c3e4f65a5727c0b104d54_b2269bd1.displayName = "Cond";
return Cond_comp_930416ad1b5c3e4f65a5727c0b104d54_b2269bd1;
})();

export const Cond_comp_5776645a648b608fffaa6d8fbe537a1a_b2269bd1 = /*#__PURE__*/ (() => {
const Cond_comp_5776645a648b608fffaa6d8fbe537a1a_b2269bd1 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state)



    return(
        (reflex___state____state__codeboxd_main___state___session____session_state.is_admin_rx_state_?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_5776645a648b608fffaa6d8fbe537a1a_b2269bd1.displayName = "Cond";
return Cond_comp_5776645a648b608fffaa6d8fbe537a1a_b2269bd1;
})();

export const Input_input_b1fb32e58023ad70e1627d618ec68a8a_b2269bd1 = /*#__PURE__*/ (() => {
const Input_input_b1fb32e58023ad70e1627d618ec68a8a_b2269bd1 = memo(({children, ...rest}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        jsx("input",{...mergeSlotProps(rest, ({ className:"admin-search-input", maxLength:40, name:"external_source", placeholder:((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.catalog_type_rx_state_?.valueOf?.() === "movie"?.valueOf?.()) ? "Fonte: tmdb" : ((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.catalog_type_rx_state_?.valueOf?.() === "series"?.valueOf?.()) ? "Fonte: tmdb" : ((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.catalog_type_rx_state_?.valueOf?.() === "book"?.valueOf?.()) ? "Fonte: openlibrary" : "Fonte: jikan ou kitsu"))), required:true }))},)
    )
});
Input_input_b1fb32e58023ad70e1627d618ec68a8a_b2269bd1.displayName = "Input";
return Input_input_b1fb32e58023ad70e1627d618ec68a8a_b2269bd1;
})();

export const Bare_comp_f4a4b36a9c19301de439bab253fd990e_b2269bd1 = /*#__PURE__*/ (() => {
const Bare_comp_f4a4b36a9c19301de439bab253fd990e_b2269bd1 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        (reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.catalog_create_loading_rx_state_ ? "Cadastrando\u2026" : "Validar e cadastrar")
    )
});
Bare_comp_f4a4b36a9c19301de439bab253fd990e_b2269bd1.displayName = "Bare";
return Bare_comp_f4a4b36a9c19301de439bab253fd990e_b2269bd1;
})();

export const Button_button_b461370334773daab7032b16e7fc658e_b2269bd1 = /*#__PURE__*/ (() => {
const Button_button_b461370334773daab7032b16e7fc658e_b2269bd1 = memo(({children, ...rest}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        jsx("button",{...mergeSlotProps(rest, ({ className:"admin-search-submit", disabled:reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.catalog_create_loading_rx_state_, type:"submit" }))},children)
    )
});
Button_button_b461370334773daab7032b16e7fc658e_b2269bd1.displayName = "Button";
return Button_button_b461370334773daab7032b16e7fc658e_b2269bd1;
})();

export const Form_form_fc8d32f88a312c61026b1106399e26c1_b2269bd1 = /*#__PURE__*/ (() => {
const Form_form_fc8d32f88a312c61026b1106399e26c1_b2269bd1 = memo(({children, ...rest}) => {
    

    const handleSubmit_ebc59d1fd6a5e47706580e13fd1bb6d7 = useCallback((ev) => {
        const $form = ev.target
        ev.preventDefault()
        const form_data = {...Object.fromEntries(new FormData($form).entries()), ...({  })};

        (((...args) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___admin____admin_state.create_catalog_item", ({ ["form"] : form_data }), ({  })))], args, ({  }))))(ev));

        if (false) {
            $form.reset()
        }
    })
    


    return(
        jsx("form",{...mergeSlotProps(rest, ({ className:"admin-catalog-create-grid", onSubmit:handleSubmit_ebc59d1fd6a5e47706580e13fd1bb6d7 }))},children)
    )
});
Form_form_fc8d32f88a312c61026b1106399e26c1_b2269bd1.displayName = "Form";
return Form_form_fc8d32f88a312c61026b1106399e26c1_b2269bd1;
})();

export const Input_input_08ca409a3924d427835d25ee67660cb9_b2269bd1 = /*#__PURE__*/ (() => {
const Input_input_08ca409a3924d427835d25ee67660cb9_b2269bd1 = memo(({children, ...rest}) => {
    const ref_admin_catalog_search = useRef(null); refs["ref_admin_catalog_search"] = ref_admin_catalog_search;
const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        jsx("input",{...mergeSlotProps(rest, ({ className:"admin-search-input", defaultValue:reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.catalog_query_rx_state_, id:"admin-catalog-search", name:"search", placeholder:"Digite o t\u00edtulo da obra", ref:ref_admin_catalog_search, type:"search" }))},)
    )
});
Input_input_08ca409a3924d427835d25ee67660cb9_b2269bd1.displayName = "Input";
return Input_input_08ca409a3924d427835d25ee67660cb9_b2269bd1;
})();

export const Bare_comp_cf02fe800ffbec386fedb60c68ba5f28_b2269bd1 = /*#__PURE__*/ (() => {
const Bare_comp_cf02fe800ffbec386fedb60c68ba5f28_b2269bd1 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        (reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.catalog_loading_rx_state_ ? "Buscando\u2026" : "Pesquisar")
    )
});
Bare_comp_cf02fe800ffbec386fedb60c68ba5f28_b2269bd1.displayName = "Bare";
return Bare_comp_cf02fe800ffbec386fedb60c68ba5f28_b2269bd1;
})();

export const Button_button_243ea5851a442ca1f5ef71e82c0fea5f_b2269bd1 = /*#__PURE__*/ (() => {
const Button_button_243ea5851a442ca1f5ef71e82c0fea5f_b2269bd1 = memo(({children, ...rest}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        jsx("button",{...mergeSlotProps(rest, ({ className:"admin-search-submit", disabled:reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.catalog_loading_rx_state_, type:"submit" }))},children)
    )
});
Button_button_243ea5851a442ca1f5ef71e82c0fea5f_b2269bd1.displayName = "Button";
return Button_button_243ea5851a442ca1f5ef71e82c0fea5f_b2269bd1;
})();

export const Form_form_f00d2df7441d21777915e9b946f9544d_b2269bd1 = /*#__PURE__*/ (() => {
const Form_form_f00d2df7441d21777915e9b946f9544d_b2269bd1 = memo(({children, ...rest}) => {
    

    const handleSubmit_2c2e0ca871c8eb494ad1b1643173a772 = useCallback((ev) => {
        const $form = ev.target
        ev.preventDefault()
        const form_data = {...Object.fromEntries(new FormData($form).entries()), ...({ ["admin_catalog_search"] : getRefValue(refs["ref_admin_catalog_search"]) })};

        (((...args) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___admin____admin_state.search_catalog", ({ ["form"] : form_data }), ({  })))], args, ({  }))))(ev));

        if (false) {
            $form.reset()
        }
    })
    


    return(
        jsx("form",{...mergeSlotProps(rest, ({ className:"admin-users-search", onSubmit:handleSubmit_2c2e0ca871c8eb494ad1b1643173a772 }))},children)
    )
});
Form_form_f00d2df7441d21777915e9b946f9544d_b2269bd1.displayName = "Form";
return Form_form_f00d2df7441d21777915e9b946f9544d_b2269bd1;
})();

export const Bare_comp_8f70128fc868d280666d8a74c59a87dc_b2269bd1 = /*#__PURE__*/ (() => {
const Bare_comp_8f70128fc868d280666d8a74c59a87dc_b2269bd1 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.catalog_error_rx_state_
    )
});
Bare_comp_8f70128fc868d280666d8a74c59a87dc_b2269bd1.displayName = "Bare";
return Bare_comp_8f70128fc868d280666d8a74c59a87dc_b2269bd1;
})();

export const Cond_comp_a7c78693771eff00795a28b79f329e24_b2269bd1 = /*#__PURE__*/ (() => {
const Cond_comp_a7c78693771eff00795a28b79f329e24_b2269bd1 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        (!((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.catalog_error_rx_state_?.valueOf?.() === ""?.valueOf?.()))?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_a7c78693771eff00795a28b79f329e24_b2269bd1.displayName = "Cond";
return Cond_comp_a7c78693771eff00795a28b79f329e24_b2269bd1;
})();

export const Bare_comp_fdfd02d9732d2aaf2010f5dbbf44089f_b2269bd1 = /*#__PURE__*/ (() => {
const Bare_comp_fdfd02d9732d2aaf2010f5dbbf44089f_b2269bd1 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.catalog_notice_rx_state_
    )
});
Bare_comp_fdfd02d9732d2aaf2010f5dbbf44089f_b2269bd1.displayName = "Bare";
return Bare_comp_fdfd02d9732d2aaf2010f5dbbf44089f_b2269bd1;
})();

export const Cond_comp_20790322da87535ef98939db23ddfa06_b2269bd1 = /*#__PURE__*/ (() => {
const Cond_comp_20790322da87535ef98939db23ddfa06_b2269bd1 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        (!((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.catalog_notice_rx_state_?.valueOf?.() === ""?.valueOf?.()))?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_20790322da87535ef98939db23ddfa06_b2269bd1.displayName = "Cond";
return Cond_comp_20790322da87535ef98939db23ddfa06_b2269bd1;
})();

export const Cond_comp_c4d0ecee12c7ab0c23df437fd0e2b3bd_b2269bd1 = /*#__PURE__*/ (() => {
const Cond_comp_c4d0ecee12c7ab0c23df437fd0e2b3bd_b2269bd1 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        (reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.catalog_loading_rx_state_?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_c4d0ecee12c7ab0c23df437fd0e2b3bd_b2269bd1.displayName = "Cond";
return Cond_comp_c4d0ecee12c7ab0c23df437fd0e2b3bd_b2269bd1;
})();

export const Bare_comp_d7ade9b87d8dcaa6b21ed7ba08e18828_b2269bd1 = /*#__PURE__*/ (() => {
const Bare_comp_d7ade9b87d8dcaa6b21ed7ba08e18828_b2269bd1 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        ("Resultados: "+(JSON.stringify(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.catalog_total_rx_state_)))
    )
});
Bare_comp_d7ade9b87d8dcaa6b21ed7ba08e18828_b2269bd1.displayName = "Bare";
return Bare_comp_d7ade9b87d8dcaa6b21ed7ba08e18828_b2269bd1;
})();

export const Foreach_comp_216f9ac93c79362fbdcf2675ac9a60b1_b2269bd1 = /*#__PURE__*/ (() => {
const Foreach_comp_216f9ac93c79362fbdcf2675ac9a60b1_b2269bd1 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        Array.prototype.map.call(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.catalog_items_rx_state_ ?? [],((item_rx_state_,index_b5b0ee279240e9326341e66994b69fa2)=>(jsx("article",{className:"admin-catalog-row",key:index_b5b0ee279240e9326341e66994b69fa2},jsx(Fragment,{},(!((item_rx_state_?.["cover_url"]?.valueOf?.() === ""?.valueOf?.()))?(jsx(Fragment,{},jsx("img",{alt:("Capa de "+item_rx_state_?.["title"]),className:"admin-catalog-cover",src:item_rx_state_?.["cover_url"]},))):(jsx(Fragment,{},jsx("div",{className:"admin-catalog-cover-empty"},jsx(LucideClapperboard,{size:20},)))))),jsx("div",{className:"admin-catalog-copy"},jsx("p",{className:"admin-user-name"},item_rx_state_?.["title"]),jsx("p",{className:"admin-user-username"},((((!((item_rx_state_?.["year"]?.valueOf?.() === ""?.valueOf?.())) ? (item_rx_state_?.["year"]+" \u00b7 ") : "")+item_rx_state_?.["external_source"])+":")+item_rx_state_?.["external_id"])),jsx("p",{className:"admin-catalog-description"},item_rx_state_?.["description"])),jsx("button",{className:"quiet-button admin-catalog-edit",onClick:((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___admin____admin_state.open_catalog_editor", ({ ["item"] : item_rx_state_ }), ({  })))], [_e], ({  })))),type:"button"},"Editar")))))
    )
});
Foreach_comp_216f9ac93c79362fbdcf2675ac9a60b1_b2269bd1.displayName = "Foreach";
return Foreach_comp_216f9ac93c79362fbdcf2675ac9a60b1_b2269bd1;
})();

export const Button_button_d8f311be1559696b30f2decadf3e3a35_b2269bd1 = /*#__PURE__*/ (() => {
const Button_button_d8f311be1559696b30f2decadf3e3a35_b2269bd1 = memo(({children, ...rest}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)
const on_click_96c22b02824eec8fce33f72775ae3cca = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___admin____admin_state.change_catalog_page", ({ ["page"] : (reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.catalog_page_rx_state_ - 1) }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent, reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state])



    return(
        jsx("button",{...mergeSlotProps(rest, ({ className:"quiet-button", disabled:(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.catalog_page_rx_state_ <= 1), onClick:on_click_96c22b02824eec8fce33f72775ae3cca, type:"button" }))},children)
    )
});
Button_button_d8f311be1559696b30f2decadf3e3a35_b2269bd1.displayName = "Button";
return Button_button_d8f311be1559696b30f2decadf3e3a35_b2269bd1;
})();

export const Bare_comp_359e8aeb649affafc24f73f4cb0fbf47_b2269bd1 = /*#__PURE__*/ (() => {
const Bare_comp_359e8aeb649affafc24f73f4cb0fbf47_b2269bd1 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        ("P\u00e1gina "+(JSON.stringify(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.catalog_page_rx_state_)))
    )
});
Bare_comp_359e8aeb649affafc24f73f4cb0fbf47_b2269bd1.displayName = "Bare";
return Bare_comp_359e8aeb649affafc24f73f4cb0fbf47_b2269bd1;
})();

export const Button_button_e7acb712640ef5de22fc13ec34eea998_b2269bd1 = /*#__PURE__*/ (() => {
const Button_button_e7acb712640ef5de22fc13ec34eea998_b2269bd1 = memo(({children, ...rest}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)
const on_click_cc16675a1c61ea57d29db79c75a5cc8d = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___admin____admin_state.change_catalog_page", ({ ["page"] : reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.catalog_next_page_rx_state_ }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent, reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state])



    return(
        jsx("button",{...mergeSlotProps(rest, ({ className:"quiet-button", disabled:(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.catalog_next_page_rx_state_?.valueOf?.() === 0?.valueOf?.()), onClick:on_click_cc16675a1c61ea57d29db79c75a5cc8d, type:"button" }))},children)
    )
});
Button_button_e7acb712640ef5de22fc13ec34eea998_b2269bd1.displayName = "Button";
return Button_button_e7acb712640ef5de22fc13ec34eea998_b2269bd1;
})();

export const Cond_comp_0df9c5ab53b49d2d72187ee4f39bc6a2_b2269bd1 = /*#__PURE__*/ (() => {
const Cond_comp_0df9c5ab53b49d2d72187ee4f39bc6a2_b2269bd1 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        (!((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.catalog_query_rx_state_?.valueOf?.() === ""?.valueOf?.()))?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_0df9c5ab53b49d2d72187ee4f39bc6a2_b2269bd1.displayName = "Cond";
return Cond_comp_0df9c5ab53b49d2d72187ee4f39bc6a2_b2269bd1;
})();

export const Cond_comp_2774a998688e3c4f73d553a226ac9d07_b2269bd1 = /*#__PURE__*/ (() => {
const Cond_comp_2774a998688e3c4f73d553a226ac9d07_b2269bd1 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        ((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.catalog_items_rx_state_.length > 0)?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_2774a998688e3c4f73d553a226ac9d07_b2269bd1.displayName = "Cond";
return Cond_comp_2774a998688e3c4f73d553a226ac9d07_b2269bd1;
})();

export const Input_input_e6535896cf503e649b81ca5576739560_b2269bd1 = /*#__PURE__*/ (() => {
const Input_input_e6535896cf503e649b81ca5576739560_b2269bd1 = memo(({children, ...rest}) => {
    const ref_catalog_edit_title = useRef(null); refs["ref_catalog_edit_title"] = ref_catalog_edit_title;
const on_change_fcdd5037e62e0dc3cf064aa2ecf7dada = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___admin____admin_state.set_catalog_edit_title", ({ ["value"] : _e?.["target"]?.["value"] }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])
const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        jsx("input",{...mergeSlotProps(rest, ({ className:"admin-search-input", id:"catalog-edit-title", maxLength:500, onChange:on_change_fcdd5037e62e0dc3cf064aa2ecf7dada, ref:ref_catalog_edit_title, value:(isNotNullOrUndefined(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.catalog_edit_title_rx_state_) ? reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.catalog_edit_title_rx_state_ : "") }))},)
    )
});
Input_input_e6535896cf503e649b81ca5576739560_b2269bd1.displayName = "Input";
return Input_input_e6535896cf503e649b81ca5576739560_b2269bd1;
})();

export const Textarea_textarea_2f40dd3e99b3ec995e7aa55792661553_b2269bd1 = /*#__PURE__*/ (() => {
const Textarea_textarea_2f40dd3e99b3ec995e7aa55792661553_b2269bd1 = memo(({children, ...rest}) => {
    const ref_catalog_edit_description = useRef(null); refs["ref_catalog_edit_description"] = ref_catalog_edit_description;
const on_change_318b2e644a4265f35d4ca1eb5d28b3c3 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___admin____admin_state.set_catalog_edit_description", ({ ["value"] : _e?.["target"]?.["value"] }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])
const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        jsx("textarea",{...mergeSlotProps(rest, ({ className:"admin-user-reason", id:"catalog-edit-description", maxLength:20000, onChange:on_change_318b2e644a4265f35d4ca1eb5d28b3c3, ref:ref_catalog_edit_description, value:reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.catalog_edit_description_rx_state_ }))},)
    )
});
Textarea_textarea_2f40dd3e99b3ec995e7aa55792661553_b2269bd1.displayName = "Textarea";
return Textarea_textarea_2f40dd3e99b3ec995e7aa55792661553_b2269bd1;
})();

export const Input_input_b50af24fa5f737c28c1b9e622f5065b5_b2269bd1 = /*#__PURE__*/ (() => {
const Input_input_b50af24fa5f737c28c1b9e622f5065b5_b2269bd1 = memo(({children, ...rest}) => {
    const ref_catalog_edit_cover = useRef(null); refs["ref_catalog_edit_cover"] = ref_catalog_edit_cover;
const on_change_bd1acf91ecf07fa018e8d515b5dd4360 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___admin____admin_state.set_catalog_edit_cover", ({ ["value"] : _e?.["target"]?.["value"] }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])
const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        jsx("input",{...mergeSlotProps(rest, ({ className:"admin-search-input", id:"catalog-edit-cover", maxLength:1000, onChange:on_change_bd1acf91ecf07fa018e8d515b5dd4360, ref:ref_catalog_edit_cover, type:"url", value:(isNotNullOrUndefined(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.catalog_edit_cover_rx_state_) ? reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.catalog_edit_cover_rx_state_ : "") }))},)
    )
});
Input_input_b50af24fa5f737c28c1b9e622f5065b5_b2269bd1.displayName = "Input";
return Input_input_b50af24fa5f737c28c1b9e622f5065b5_b2269bd1;
})();

export const Input_input_0766c55c957c0fef6f57a3fe57f35edd_b2269bd1 = /*#__PURE__*/ (() => {
const Input_input_0766c55c957c0fef6f57a3fe57f35edd_b2269bd1 = memo(({children, ...rest}) => {
    const ref_catalog_edit_year = useRef(null); refs["ref_catalog_edit_year"] = ref_catalog_edit_year;
const on_change_259638a507a07cbcaeee2342e36c0a7d = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___admin____admin_state.set_catalog_edit_year", ({ ["value"] : _e?.["target"]?.["value"] }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])
const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        jsx("input",{...mergeSlotProps(rest, ({ className:"admin-search-input", id:"catalog-edit-year", inputMode:"numeric", maxLength:4, onChange:on_change_259638a507a07cbcaeee2342e36c0a7d, ref:ref_catalog_edit_year, type:"text", value:(isNotNullOrUndefined(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.catalog_edit_year_rx_state_) ? reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.catalog_edit_year_rx_state_ : "") }))},)
    )
});
Input_input_0766c55c957c0fef6f57a3fe57f35edd_b2269bd1.displayName = "Input";
return Input_input_0766c55c957c0fef6f57a3fe57f35edd_b2269bd1;
})();

export const Button_button_99ceb6212f65e286c190562007deb6e4_b2269bd1 = /*#__PURE__*/ (() => {
const Button_button_99ceb6212f65e286c190562007deb6e4_b2269bd1 = memo(({children, ...rest}) => {
    const on_click_d39dbabbc20d61688303618a79660644 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___admin____admin_state.close_catalog_editor", ({  }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])
const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        jsx("button",{...mergeSlotProps(rest, ({ className:"quiet-button", disabled:reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.catalog_edit_loading_rx_state_, onClick:on_click_d39dbabbc20d61688303618a79660644, type:"button" }))},children)
    )
});
Button_button_99ceb6212f65e286c190562007deb6e4_b2269bd1.displayName = "Button";
return Button_button_99ceb6212f65e286c190562007deb6e4_b2269bd1;
})();

export const Bare_comp_8fdd94ec92d759262a83c71766a129b3_b2269bd1 = /*#__PURE__*/ (() => {
const Bare_comp_8fdd94ec92d759262a83c71766a129b3_b2269bd1 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        (reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.catalog_edit_loading_rx_state_ ? "Salvando\u2026" : "Salvar altera\u00e7\u00f5es")
    )
});
Bare_comp_8fdd94ec92d759262a83c71766a129b3_b2269bd1.displayName = "Bare";
return Bare_comp_8fdd94ec92d759262a83c71766a129b3_b2269bd1;
})();

export const Button_button_6ed3f7c21eafbc9c6582670f9e203325_b2269bd1 = /*#__PURE__*/ (() => {
const Button_button_6ed3f7c21eafbc9c6582670f9e203325_b2269bd1 = memo(({children, ...rest}) => {
    const on_click_73cb78efc156b5c1667e5681e1a9532f = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___admin____admin_state.save_catalog_edit", ({  }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])
const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        jsx("button",{...mergeSlotProps(rest, ({ className:"admin-dialog-confirm", disabled:reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.catalog_edit_loading_rx_state_, onClick:on_click_73cb78efc156b5c1667e5681e1a9532f, type:"button" }))},children)
    )
});
Button_button_6ed3f7c21eafbc9c6582670f9e203325_b2269bd1.displayName = "Button";
return Button_button_6ed3f7c21eafbc9c6582670f9e203325_b2269bd1;
})();

export const Form_form_478de0e86c0d5d44a490168b87fe35fb_b2269bd1 = /*#__PURE__*/ (() => {
const Form_form_478de0e86c0d5d44a490168b87fe35fb_b2269bd1 = memo(({children, ...rest}) => {
    

    const handleSubmit_c92dde6c9842b749f438ce9dc71bd8b7 = useCallback((ev) => {
        const $form = ev.target
        ev.preventDefault()
        const form_data = {...Object.fromEntries(new FormData($form).entries()), ...({ ["catalog_edit_title"] : getRefValue(refs["ref_catalog_edit_title"]), ["catalog_edit_description"] : getRefValue(refs["ref_catalog_edit_description"]), ["catalog_edit_cover"] : getRefValue(refs["ref_catalog_edit_cover"]), ["catalog_edit_year"] : getRefValue(refs["ref_catalog_edit_year"]) })};

        (((...args) => (addEvents([(ReflexEvent("_call_function", ({ ["function"] : (() => null), ["callback"] : null }), ({ ["preventDefault"] : true })))], args, ({  }))))(ev));

        if (false) {
            $form.reset()
        }
    })
    


    return(
        jsx("form",{...mergeSlotProps(rest, ({ "aria-label":"Editar obra do cat\u00e1logo", "aria-modal":"true", className:"admin-confirm-dialog admin-catalog-editor", onSubmit:handleSubmit_c92dde6c9842b749f438ce9dc71bd8b7, role:"dialog" }))},children)
    )
});
Form_form_478de0e86c0d5d44a490168b87fe35fb_b2269bd1.displayName = "Form";
return Form_form_478de0e86c0d5d44a490168b87fe35fb_b2269bd1;
})();

export const Cond_comp_1a11e6105415d0d6b4bc5d1d5148a543_b2269bd1 = /*#__PURE__*/ (() => {
const Cond_comp_1a11e6105415d0d6b4bc5d1d5148a543_b2269bd1 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        (!((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.catalog_edit_id_rx_state_?.valueOf?.() === ""?.valueOf?.()))?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_1a11e6105415d0d6b4bc5d1d5148a543_b2269bd1.displayName = "Cond";
return Cond_comp_1a11e6105415d0d6b4bc5d1d5148a543_b2269bd1;
})();
