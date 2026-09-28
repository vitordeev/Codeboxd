
import {ReflexEvent,applyEventActions,getRefValue,getRefValues,isNotNullOrUndefined,isTrue,refs} from "$/utils/state"
import {StateContexts,addEvents} from "$/utils/context"
import {Fragment,memo,useCallback,useContext,useEffect,useRef} from "react"
import {jsx} from "@emotion/react"
import LucideMessageSquareText from "lucide-react/dist/esm/icons/message-square-text.mjs"
import LucideClapperboard from "lucide-react/dist/esm/icons/clapperboard.mjs"








export const Button_button_d90e5b647b2134a86260a89d863d1ca1_b2269bd1 = memo(({children}) => {
    const on_click_04fd11fb12f6e03482bf1190dac1510d = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.logout", ({  }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])



    return(
        jsx("button",{className:"quiet-button admin-logout-button",onClick:on_click_04fd11fb12f6e03482bf1190dac1510d,type:"button"},children)
    )
});
Button_button_d90e5b647b2134a86260a89d863d1ca1_b2269bd1.displayName = "Button";

export const Bare_comp_4abda207c114d110848eb7bcf9c2fb41_b2269bd1 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        ("Atualizado em "+reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.dashboard_updated_at_rx_state_)
    )
});
Bare_comp_4abda207c114d110848eb7bcf9c2fb41_b2269bd1.displayName = "Bare";

export const Cond_comp_0e2c2448aee9d00a565c77db3652aad4_b2269bd1 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        (!((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.dashboard_updated_at_rx_state_?.valueOf?.() === ""?.valueOf?.()))?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_0e2c2448aee9d00a565c77db3652aad4_b2269bd1.displayName = "Cond";

export const Bare_comp_fe21bfb499eb75543713d5a5e5937abe_b2269bd1 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        (reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.dashboard_loading_rx_state_ ? "Atualizando\u2026" : "Atualizar")
    )
});
Bare_comp_fe21bfb499eb75543713d5a5e5937abe_b2269bd1.displayName = "Bare";

export const Button_button_2bdd8540ce8a643a02e825ac2f431c40_b2269bd1 = memo(({children}) => {
    const on_click_4360fdbadb815f1833c2d70aa17fd402 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___admin____admin_state.load_dashboard", ({  }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])
const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        jsx("button",{className:"quiet-button admin-refresh-button",disabled:reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.dashboard_loading_rx_state_,onClick:on_click_4360fdbadb815f1833c2d70aa17fd402,type:"button"},children)
    )
});
Button_button_2bdd8540ce8a643a02e825ac2f431c40_b2269bd1.displayName = "Button";

export const Bare_comp_762e5789488d7349b875df78152af078_b2269bd1 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.dashboard_error_rx_state_
    )
});
Bare_comp_762e5789488d7349b875df78152af078_b2269bd1.displayName = "Bare";

export const Cond_comp_bfdf6fcdecf05fdaa6b1dc799008d033_b2269bd1 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        (!((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.dashboard_error_rx_state_?.valueOf?.() === ""?.valueOf?.()))?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_bfdf6fcdecf05fdaa6b1dc799008d033_b2269bd1.displayName = "Cond";

export const Cond_comp_b2f7c0fc4ff3084c2dca39b172f51cc4_b2269bd1 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        (reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.dashboard_loading_rx_state_?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_b2f7c0fc4ff3084c2dca39b172f51cc4_b2269bd1.displayName = "Cond";

export const Bare_comp_5ade1cb7ca19878d1110e1aebbfc93a3_b2269bd1 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.dashboard_stats_rx_state_?.["users_total"]
    )
});
Bare_comp_5ade1cb7ca19878d1110e1aebbfc93a3_b2269bd1.displayName = "Bare";

export const Bare_comp_1daebcb537606c2d5a710e01c47725ec_b2269bd1 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.dashboard_stats_rx_state_?.["posts_total"]
    )
});
Bare_comp_1daebcb537606c2d5a710e01c47725ec_b2269bd1.displayName = "Bare";

export const Bare_comp_dc71dea2eef0f989c648a6a0615967f0_b2269bd1 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.dashboard_stats_rx_state_?.["media_total"]
    )
});
Bare_comp_dc71dea2eef0f989c648a6a0615967f0_b2269bd1.displayName = "Bare";

export const Bare_comp_bd69dd714ef0b9a26f170038ac3a4037_b2269bd1 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.dashboard_stats_rx_state_?.["reports_pending"]
    )
});
Bare_comp_bd69dd714ef0b9a26f170038ac3a4037_b2269bd1.displayName = "Bare";

export const Foreach_comp_34f09104a9c63e43b8c380fa6a0cfe65_b2269bd1 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        Array.prototype.map.call(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.pending_reports_rx_state_ ?? [],((item_rx_state_,index_952059cd3d946d65e3d06d7728c36a73)=>(jsx("li",{className:"admin-activity-item",key:index_952059cd3d946d65e3d06d7728c36a73},jsx("div",{className:"admin-activity-row"},jsx("p",{className:"admin-activity-title"},((("Report #"+item_rx_state_?.["id"])+" \u00b7 ")+item_rx_state_?.["target_type"])),jsx("p",{className:"admin-activity-detail"},("Motivo: "+item_rx_state_?.["reason"])),jsx("time",{className:"admin-activity-time"},item_rx_state_?.["created_at"]))))))
    )
});
Foreach_comp_34f09104a9c63e43b8c380fa6a0cfe65_b2269bd1.displayName = "Foreach";

export const Cond_comp_214db5d85a69eaa608d9e16de713f989_b2269bd1 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        ((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.pending_reports_rx_state_.length > 0)?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_214db5d85a69eaa608d9e16de713f989_b2269bd1.displayName = "Cond";

export const Foreach_comp_1935ce42c8b0decd553b8428f2069fcc_b2269bd1 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        Array.prototype.map.call(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.recent_posts_rx_state_ ?? [],((item_rx_state_,index_e46c22ad3799a5475860d89427f6398b)=>(jsx("li",{className:"admin-activity-item",key:index_e46c22ad3799a5475860d89427f6398b},jsx("div",{className:"admin-activity-row"},jsx("div",{className:"admin-activity-icon"},jsx(LucideMessageSquareText,{size:18},)),jsx("div",{},jsx("p",{className:"admin-activity-title"},("Publica\u00e7\u00e3o #"+item_rx_state_?.["id"])),jsx("p",{className:"admin-activity-detail"},("Usu\u00e1rio #"+item_rx_state_?.["user_id"]))),jsx("time",{className:"admin-activity-time"},item_rx_state_?.["created_at"]))))))
    )
});
Foreach_comp_1935ce42c8b0decd553b8428f2069fcc_b2269bd1.displayName = "Foreach";

export const Cond_comp_71009c5bf882be6ea4c431a72dcfecb3_b2269bd1 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        ((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.recent_posts_rx_state_.length > 0)?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_71009c5bf882be6ea4c431a72dcfecb3_b2269bd1.displayName = "Cond";

export const Cond_comp_8aa28e5a6ba1c8e6245e75442827384d_b2269bd1 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state)



    return(
        (reflex___state____state__codeboxd_main___state___session____session_state.is_admin_rx_state_?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_8aa28e5a6ba1c8e6245e75442827384d_b2269bd1.displayName = "Cond";

export const Input_input_c22ad2cc122832e1aef927ece278f806_b2269bd1 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        jsx("input",{className:"admin-search-input",maxLength:40,name:"external_source",placeholder:((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.catalog_type_rx_state_?.valueOf?.() === "movie"?.valueOf?.()) ? "Fonte: tmdb" : ((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.catalog_type_rx_state_?.valueOf?.() === "series"?.valueOf?.()) ? "Fonte: tmdb" : ((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.catalog_type_rx_state_?.valueOf?.() === "book"?.valueOf?.()) ? "Fonte: openlibrary" : "Fonte: jikan ou kitsu"))),required:true},)
    )
});
Input_input_c22ad2cc122832e1aef927ece278f806_b2269bd1.displayName = "Input";

export const Bare_comp_d298626a2e0f02fae9ea125904b72de6_b2269bd1 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        (reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.catalog_create_loading_rx_state_ ? "Cadastrando\u2026" : "Validar e cadastrar")
    )
});
Bare_comp_d298626a2e0f02fae9ea125904b72de6_b2269bd1.displayName = "Bare";

export const Button_button_20a2c2092886fa345972b3e5dbf0e999_b2269bd1 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        jsx("button",{className:"admin-search-submit",disabled:reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.catalog_create_loading_rx_state_,type:"submit"},children)
    )
});
Button_button_20a2c2092886fa345972b3e5dbf0e999_b2269bd1.displayName = "Button";

export const Form_form_ce373ac14813739bedd8cc327a44bf97_b2269bd1 = memo(({children}) => {
    

    const handleSubmit_0f38c1b1ccd728cc8551471b367c6570 = useCallback((ev) => {
        const $form = ev.target
        ev.preventDefault()
        const form_data = {...Object.fromEntries(new FormData($form).entries()), ...({  })};

        (((...args) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___admin____admin_state.create_catalog_item", ({ ["form"] : form_data }), ({  })))], args, ({  }))))(ev));

        if (false) {
            $form.reset()
        }
    })
    


    return(
        jsx("form",{className:"admin-catalog-create-grid",onSubmit:handleSubmit_0f38c1b1ccd728cc8551471b367c6570},children)
    )
});
Form_form_ce373ac14813739bedd8cc327a44bf97_b2269bd1.displayName = "Form";

export const Input_input_30c09a07583f193846be11550daa4016_b2269bd1 = memo(({children}) => {
    const ref_admin_catalog_search = useRef(null); refs["ref_admin_catalog_search"] = ref_admin_catalog_search;
const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        jsx("input",{className:"admin-search-input",defaultValue:reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.catalog_query_rx_state_,id:"admin-catalog-search",name:"search",placeholder:"Digite o t\u00edtulo da obra",ref:ref_admin_catalog_search,type:"search"},)
    )
});
Input_input_30c09a07583f193846be11550daa4016_b2269bd1.displayName = "Input";

export const Bare_comp_009a94013da08c5c751121d484ce7926_b2269bd1 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        (reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.catalog_loading_rx_state_ ? "Buscando\u2026" : "Pesquisar")
    )
});
Bare_comp_009a94013da08c5c751121d484ce7926_b2269bd1.displayName = "Bare";

export const Button_button_ce51fcfab09b042c57ea81c33089ed6a_b2269bd1 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        jsx("button",{className:"admin-search-submit",disabled:reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.catalog_loading_rx_state_,type:"submit"},children)
    )
});
Button_button_ce51fcfab09b042c57ea81c33089ed6a_b2269bd1.displayName = "Button";

export const Form_form_41a625f30745740e06f89f8199efd9fa_b2269bd1 = memo(({children}) => {
    

    const handleSubmit_07c5266550f522873ad40704e6b69411 = useCallback((ev) => {
        const $form = ev.target
        ev.preventDefault()
        const form_data = {...Object.fromEntries(new FormData($form).entries()), ...({ ["admin_catalog_search"] : getRefValue(refs["ref_admin_catalog_search"]) })};

        (((...args) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___admin____admin_state.search_catalog", ({ ["form"] : form_data }), ({  })))], args, ({  }))))(ev));

        if (false) {
            $form.reset()
        }
    })
    


    return(
        jsx("form",{className:"admin-users-search",onSubmit:handleSubmit_07c5266550f522873ad40704e6b69411},children)
    )
});
Form_form_41a625f30745740e06f89f8199efd9fa_b2269bd1.displayName = "Form";

export const Bare_comp_0db43a230272c2d71000efa2933c7ef7_b2269bd1 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.catalog_error_rx_state_
    )
});
Bare_comp_0db43a230272c2d71000efa2933c7ef7_b2269bd1.displayName = "Bare";

export const Cond_comp_8e035709268d26f1eaac7a85a8a3b02d_b2269bd1 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        (!((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.catalog_error_rx_state_?.valueOf?.() === ""?.valueOf?.()))?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_8e035709268d26f1eaac7a85a8a3b02d_b2269bd1.displayName = "Cond";

export const Bare_comp_4f348bd22cea0d8c1985ed93e382661f_b2269bd1 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.catalog_notice_rx_state_
    )
});
Bare_comp_4f348bd22cea0d8c1985ed93e382661f_b2269bd1.displayName = "Bare";

export const Cond_comp_997deaa5f9962d0bf97ca2f5d210dcb7_b2269bd1 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        (!((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.catalog_notice_rx_state_?.valueOf?.() === ""?.valueOf?.()))?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_997deaa5f9962d0bf97ca2f5d210dcb7_b2269bd1.displayName = "Cond";

export const Cond_comp_668e3aa2dcee53a4c6acc802da87f7d0_b2269bd1 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        (reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.catalog_loading_rx_state_?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_668e3aa2dcee53a4c6acc802da87f7d0_b2269bd1.displayName = "Cond";

export const Bare_comp_21d86c89b72340f3ef8d5ad0547b26e1_b2269bd1 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        ("Resultados: "+(JSON.stringify(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.catalog_total_rx_state_)))
    )
});
Bare_comp_21d86c89b72340f3ef8d5ad0547b26e1_b2269bd1.displayName = "Bare";

export const Foreach_comp_b93b520da431914e1fa608f5f072e612_b2269bd1 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        Array.prototype.map.call(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.catalog_items_rx_state_ ?? [],((item_rx_state_,index_a609939404cd39ec7b06618926a149cb)=>(jsx("article",{className:"admin-catalog-row",key:index_a609939404cd39ec7b06618926a149cb},jsx(Fragment,{},(!((item_rx_state_?.["cover_url"]?.valueOf?.() === ""?.valueOf?.()))?(jsx(Fragment,{},jsx("img",{alt:("Capa de "+item_rx_state_?.["title"]),className:"admin-catalog-cover",src:item_rx_state_?.["cover_url"]},))):(jsx(Fragment,{},jsx("div",{className:"admin-catalog-cover-empty"},jsx(LucideClapperboard,{size:20},)))))),jsx("div",{className:"admin-catalog-copy"},jsx("p",{className:"admin-user-name"},item_rx_state_?.["title"]),jsx("p",{className:"admin-user-username"},((((!((item_rx_state_?.["year"]?.valueOf?.() === ""?.valueOf?.())) ? (item_rx_state_?.["year"]+" \u00b7 ") : "")+item_rx_state_?.["external_source"])+":")+item_rx_state_?.["external_id"])),jsx("p",{className:"admin-catalog-description"},item_rx_state_?.["description"])),jsx("button",{className:"quiet-button admin-catalog-edit",onClick:((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___admin____admin_state.open_catalog_editor", ({ ["item"] : item_rx_state_ }), ({  })))], [_e], ({  })))),type:"button"},"Editar")))))
    )
});
Foreach_comp_b93b520da431914e1fa608f5f072e612_b2269bd1.displayName = "Foreach";

export const Button_button_89c525ec3111603b6801aad0b7da3e67_b2269bd1 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)
const on_click_96c22b02824eec8fce33f72775ae3cca = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___admin____admin_state.change_catalog_page", ({ ["page"] : (reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.catalog_page_rx_state_ - 1) }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent, reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state])



    return(
        jsx("button",{className:"quiet-button",disabled:(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.catalog_page_rx_state_ <= 1),onClick:on_click_96c22b02824eec8fce33f72775ae3cca,type:"button"},children)
    )
});
Button_button_89c525ec3111603b6801aad0b7da3e67_b2269bd1.displayName = "Button";

export const Bare_comp_be7085535503f9428e48e11276eb9cde_b2269bd1 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        ("P\u00e1gina "+(JSON.stringify(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.catalog_page_rx_state_)))
    )
});
Bare_comp_be7085535503f9428e48e11276eb9cde_b2269bd1.displayName = "Bare";

export const Button_button_b9ec93232d0db0f65e0a56e53fcdb2c1_b2269bd1 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)
const on_click_cc16675a1c61ea57d29db79c75a5cc8d = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___admin____admin_state.change_catalog_page", ({ ["page"] : reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.catalog_next_page_rx_state_ }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent, reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state])



    return(
        jsx("button",{className:"quiet-button",disabled:(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.catalog_next_page_rx_state_?.valueOf?.() === 0?.valueOf?.()),onClick:on_click_cc16675a1c61ea57d29db79c75a5cc8d,type:"button"},children)
    )
});
Button_button_b9ec93232d0db0f65e0a56e53fcdb2c1_b2269bd1.displayName = "Button";

export const Cond_comp_3a52f7f7782d643ff20f8a2e5fa893e5_b2269bd1 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        (!((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.catalog_query_rx_state_?.valueOf?.() === ""?.valueOf?.()))?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_3a52f7f7782d643ff20f8a2e5fa893e5_b2269bd1.displayName = "Cond";

export const Cond_comp_1131f0c61a6be531fec9ad353e04d136_b2269bd1 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        ((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.catalog_items_rx_state_.length > 0)?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_1131f0c61a6be531fec9ad353e04d136_b2269bd1.displayName = "Cond";

export const Input_input_81fab64d139a109f04e68a4b0bd56d47_b2269bd1 = memo(({children}) => {
    const ref_catalog_edit_title = useRef(null); refs["ref_catalog_edit_title"] = ref_catalog_edit_title;
const on_change_fcdd5037e62e0dc3cf064aa2ecf7dada = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___admin____admin_state.set_catalog_edit_title", ({ ["value"] : _e?.["target"]?.["value"] }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])
const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        jsx("input",{className:"admin-search-input",id:"catalog-edit-title",maxLength:500,onChange:on_change_fcdd5037e62e0dc3cf064aa2ecf7dada,ref:ref_catalog_edit_title,value:(isNotNullOrUndefined(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.catalog_edit_title_rx_state_) ? reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.catalog_edit_title_rx_state_ : "")},)
    )
});
Input_input_81fab64d139a109f04e68a4b0bd56d47_b2269bd1.displayName = "Input";

export const Textarea_textarea_e1277803127653725db4b6750245d06b_b2269bd1 = memo(({children}) => {
    const ref_catalog_edit_description = useRef(null); refs["ref_catalog_edit_description"] = ref_catalog_edit_description;
const on_change_318b2e644a4265f35d4ca1eb5d28b3c3 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___admin____admin_state.set_catalog_edit_description", ({ ["value"] : _e?.["target"]?.["value"] }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])
const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        jsx("textarea",{className:"admin-user-reason",id:"catalog-edit-description",maxLength:20000,onChange:on_change_318b2e644a4265f35d4ca1eb5d28b3c3,ref:ref_catalog_edit_description,value:reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.catalog_edit_description_rx_state_},)
    )
});
Textarea_textarea_e1277803127653725db4b6750245d06b_b2269bd1.displayName = "Textarea";

export const Input_input_5bc2cbefb75e12a45dfae63aa0dd1a31_b2269bd1 = memo(({children}) => {
    const ref_catalog_edit_cover = useRef(null); refs["ref_catalog_edit_cover"] = ref_catalog_edit_cover;
const on_change_bd1acf91ecf07fa018e8d515b5dd4360 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___admin____admin_state.set_catalog_edit_cover", ({ ["value"] : _e?.["target"]?.["value"] }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])
const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        jsx("input",{className:"admin-search-input",id:"catalog-edit-cover",maxLength:1000,onChange:on_change_bd1acf91ecf07fa018e8d515b5dd4360,ref:ref_catalog_edit_cover,type:"url",value:(isNotNullOrUndefined(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.catalog_edit_cover_rx_state_) ? reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.catalog_edit_cover_rx_state_ : "")},)
    )
});
Input_input_5bc2cbefb75e12a45dfae63aa0dd1a31_b2269bd1.displayName = "Input";

export const Input_input_24445070c04532cdbddda88d97445415_b2269bd1 = memo(({children}) => {
    const ref_catalog_edit_year = useRef(null); refs["ref_catalog_edit_year"] = ref_catalog_edit_year;
const on_change_259638a507a07cbcaeee2342e36c0a7d = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___admin____admin_state.set_catalog_edit_year", ({ ["value"] : _e?.["target"]?.["value"] }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])
const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        jsx("input",{className:"admin-search-input",id:"catalog-edit-year",inputMode:"numeric",maxLength:4,onChange:on_change_259638a507a07cbcaeee2342e36c0a7d,ref:ref_catalog_edit_year,type:"text",value:(isNotNullOrUndefined(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.catalog_edit_year_rx_state_) ? reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.catalog_edit_year_rx_state_ : "")},)
    )
});
Input_input_24445070c04532cdbddda88d97445415_b2269bd1.displayName = "Input";

export const Button_button_2dbff00573999b0a8b6a229d91f342f0_b2269bd1 = memo(({children}) => {
    const on_click_d39dbabbc20d61688303618a79660644 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___admin____admin_state.close_catalog_editor", ({  }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])
const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        jsx("button",{className:"quiet-button",disabled:reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.catalog_edit_loading_rx_state_,onClick:on_click_d39dbabbc20d61688303618a79660644,type:"button"},children)
    )
});
Button_button_2dbff00573999b0a8b6a229d91f342f0_b2269bd1.displayName = "Button";

export const Bare_comp_8e43e97ced825733fcefee73022b0cb1_b2269bd1 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        (reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.catalog_edit_loading_rx_state_ ? "Salvando\u2026" : "Salvar altera\u00e7\u00f5es")
    )
});
Bare_comp_8e43e97ced825733fcefee73022b0cb1_b2269bd1.displayName = "Bare";

export const Button_button_bfa2b04d2dab0499ef6f4957e5725c03_b2269bd1 = memo(({children}) => {
    const on_click_73cb78efc156b5c1667e5681e1a9532f = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___admin____admin_state.save_catalog_edit", ({  }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])
const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        jsx("button",{className:"admin-dialog-confirm",disabled:reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.catalog_edit_loading_rx_state_,onClick:on_click_73cb78efc156b5c1667e5681e1a9532f,type:"button"},children)
    )
});
Button_button_bfa2b04d2dab0499ef6f4957e5725c03_b2269bd1.displayName = "Button";

export const Form_form_9ac0ddca669638fc474510b22d345250_b2269bd1 = memo(({children}) => {
    

    const handleSubmit_b0da2e8abe22772dfdb552b2eec97c3a = useCallback((ev) => {
        const $form = ev.target
        ev.preventDefault()
        const form_data = {...Object.fromEntries(new FormData($form).entries()), ...({ ["catalog_edit_title"] : getRefValue(refs["ref_catalog_edit_title"]), ["catalog_edit_description"] : getRefValue(refs["ref_catalog_edit_description"]), ["catalog_edit_cover"] : getRefValue(refs["ref_catalog_edit_cover"]), ["catalog_edit_year"] : getRefValue(refs["ref_catalog_edit_year"]) })};

        (((...args) => (addEvents([(ReflexEvent("_call_function", ({ ["function"] : (() => null), ["callback"] : null }), ({ ["preventDefault"] : true })))], args, ({  }))))(ev));

        if (false) {
            $form.reset()
        }
    })
    


    return(
        jsx("form",{"aria-label":"Editar obra do cat\u00e1logo","aria-modal":"true",className:"admin-confirm-dialog admin-catalog-editor",onSubmit:handleSubmit_b0da2e8abe22772dfdb552b2eec97c3a,role:"dialog"},children)
    )
});
Form_form_9ac0ddca669638fc474510b22d345250_b2269bd1.displayName = "Form";

export const Cond_comp_d735d1a9f93c91fceae93f0aac5656b7_b2269bd1 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        (!((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.catalog_edit_id_rx_state_?.valueOf?.() === ""?.valueOf?.()))?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_d735d1a9f93c91fceae93f0aac5656b7_b2269bd1.displayName = "Cond";
