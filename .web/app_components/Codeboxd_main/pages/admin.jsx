
import {ReflexEvent,applyEventActions,getRefValue,getRefValues,isTrue,refs} from "$/utils/state"
import {Fragment,memo,useCallback,useContext,useEffect,useRef} from "react"
import {StateContexts,addEvents} from "$/utils/context"
import {jsx} from "@emotion/react"
import {DynamicIcon} from "lucide-react/dynamic.mjs"








export const Input_input_531865e9a11759a5188ffabe009a6422_27fd17d6 = memo(({children}) => {
    const ref_admin_password = useRef(null); refs["ref_admin_password"] = ref_admin_password;
const reflex___state____state__codeboxd_main___state___session____session_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state)



    return(
        jsx("input",{autoComplete:"current-password",className:"admin-login-input admin-password-input",id:"admin_password",name:"password",placeholder:"Sua senha",ref:ref_admin_password,required:true,type:(reflex___state____state__codeboxd_main___state___session____session_state.admin_password_visible_rx_state_ ? "text" : "password")},)
    )
});
Input_input_531865e9a11759a5188ffabe009a6422_27fd17d6.displayName = "Input";

export const Dynamicicon_dynamicicon_ac530eeee0a26e6f0f2e534b611544cf_27fd17d6 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state)



    return(
        jsx(DynamicIcon,{name:(reflex___state____state__codeboxd_main___state___session____session_state.admin_password_visible_rx_state_ ? "eye-off" : "eye").replaceAll("_", "-"),size:18},)
    )
});
Dynamicicon_dynamicicon_ac530eeee0a26e6f0f2e534b611544cf_27fd17d6.displayName = "DynamicIcon";

export const Button_button_d65dd17558c5527c576be3b0fe1c1843_27fd17d6 = memo(({children}) => {
    const on_click_fa97716112163c9dbf5dad0e92987b4b = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.toggle_admin_password", ({  }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])
const reflex___state____state__codeboxd_main___state___session____session_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state)



    return(
        jsx("button",{"aria-label":(reflex___state____state__codeboxd_main___state___session____session_state.admin_password_visible_rx_state_ ? "Ocultar senha" : "Mostrar senha"),className:"admin-password-toggle",onClick:on_click_fa97716112163c9dbf5dad0e92987b4b,type:"button"},children)
    )
});
Button_button_d65dd17558c5527c576be3b0fe1c1843_27fd17d6.displayName = "Button";

export const Bare_comp_bd554523900b9b74daaac23eac57e50a_27fd17d6 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state)



    return(
        reflex___state____state__codeboxd_main___state___session____session_state.error_message_rx_state_
    )
});
Bare_comp_bd554523900b9b74daaac23eac57e50a_27fd17d6.displayName = "Bare";

export const Cond_comp_d2b0fe9982d8d79ffc1f395127db034c_27fd17d6 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state)



    return(
        (!((reflex___state____state__codeboxd_main___state___session____session_state.error_message_rx_state_?.valueOf?.() === ""?.valueOf?.()))?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_d2b0fe9982d8d79ffc1f395127db034c_27fd17d6.displayName = "Cond";

export const Bare_comp_8d0d0dbe9e52451ab479605fae6a66af_27fd17d6 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state)



    return(
        (reflex___state____state__codeboxd_main___state___session____session_state.is_loading_rx_state_ ? "Verificando acesso\u2026" : "Entrar na administra\u00e7\u00e3o")
    )
});
Bare_comp_8d0d0dbe9e52451ab479605fae6a66af_27fd17d6.displayName = "Bare";

export const Button_button_a65a61e4175cca1466521caec7ff335a_27fd17d6 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state)



    return(
        jsx("button",{className:"admin-login-submit",disabled:reflex___state____state__codeboxd_main___state___session____session_state.is_loading_rx_state_,type:"submit"},children)
    )
});
Button_button_a65a61e4175cca1466521caec7ff335a_27fd17d6.displayName = "Button";

export const Form_form_471d8f94ea188278ade7d000a265231b_27fd17d6 = memo(({children}) => {
    

    const handleSubmit_80f342a7b6a4aeac7769dc6f788d2692 = useCallback((ev) => {
        const $form = ev.target
        ev.preventDefault()
        const form_data = {...Object.fromEntries(new FormData($form).entries()), ...({ ["admin_email"] : getRefValue(refs["ref_admin_email"]), ["admin_password"] : getRefValue(refs["ref_admin_password"]) })};

        (((...args) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.admin_login", ({ ["form"] : form_data }), ({  })))], args, ({  }))))(ev));

        if (false) {
            $form.reset()
        }
    })
    


    return(
        jsx("form",{className:"admin-login-form",onSubmit:handleSubmit_80f342a7b6a4aeac7769dc6f788d2692},children)
    )
});
Form_form_471d8f94ea188278ade7d000a265231b_27fd17d6.displayName = "Form";

export const Button_button_d90e5b647b2134a86260a89d863d1ca1_27fd17d6 = memo(({children}) => {
    const on_click_04fd11fb12f6e03482bf1190dac1510d = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.logout", ({  }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])



    return(
        jsx("button",{className:"quiet-button admin-logout-button",onClick:on_click_04fd11fb12f6e03482bf1190dac1510d,type:"button"},children)
    )
});
Button_button_d90e5b647b2134a86260a89d863d1ca1_27fd17d6.displayName = "Button";

export const Input_input_54af312893eb5e9ebcf3ba06874d8819_27fd17d6 = memo(({children}) => {
    const ref_admin_user_search = useRef(null); refs["ref_admin_user_search"] = ref_admin_user_search;
const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        jsx("input",{className:"admin-search-input",defaultValue:reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.users_query_rx_state_,id:"admin-user-search",name:"search",placeholder:"Ex.: nome de usu\u00e1rio ou 123",ref:ref_admin_user_search,required:true,type:"search"},)
    )
});
Input_input_54af312893eb5e9ebcf3ba06874d8819_27fd17d6.displayName = "Input";

export const Select_select_2b61f3442fd21b987b355a75dedf4cd1_27fd17d6 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        jsx("select",{className:"admin-search-select",defaultValue:reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.users_status_filter_rx_state_,name:"account_status"},children)
    )
});
Select_select_2b61f3442fd21b987b355a75dedf4cd1_27fd17d6.displayName = "Select";

export const Select_select_08aa46a1e2a413b6906c9d9599b4a030_27fd17d6 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        jsx("select",{className:"admin-search-select",defaultValue:reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.users_role_filter_rx_state_,name:"role"},children)
    )
});
Select_select_08aa46a1e2a413b6906c9d9599b4a030_27fd17d6.displayName = "Select";

export const Bare_comp_1eda7ed3712c26b99a225b9b52600b31_27fd17d6 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        (reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.users_loading_rx_state_ ? "Buscando\u2026" : "Pesquisar")
    )
});
Bare_comp_1eda7ed3712c26b99a225b9b52600b31_27fd17d6.displayName = "Bare";

export const Button_button_7982174bffbfc34c36953f89cc4595a0_27fd17d6 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        jsx("button",{className:"admin-search-submit",disabled:reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.users_loading_rx_state_,type:"submit"},children)
    )
});
Button_button_7982174bffbfc34c36953f89cc4595a0_27fd17d6.displayName = "Button";

export const Form_form_ffd707b6b2370ef1f70c30e8099edb23_27fd17d6 = memo(({children}) => {
    

    const handleSubmit_03fb1725d66bdcc69ca5a177df548644 = useCallback((ev) => {
        const $form = ev.target
        ev.preventDefault()
        const form_data = {...Object.fromEntries(new FormData($form).entries()), ...({ ["admin_user_search"] : getRefValue(refs["ref_admin_user_search"]) })};

        (((...args) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___admin____admin_state.search_users", ({ ["form"] : form_data }), ({  })))], args, ({  }))))(ev));

        if (false) {
            $form.reset()
        }
    })
    


    return(
        jsx("form",{className:"admin-users-search",onSubmit:handleSubmit_03fb1725d66bdcc69ca5a177df548644},children)
    )
});
Form_form_ffd707b6b2370ef1f70c30e8099edb23_27fd17d6.displayName = "Form";

export const Bare_comp_53f3fe298e3610aa715c6d3f334154c9_27fd17d6 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.users_error_rx_state_
    )
});
Bare_comp_53f3fe298e3610aa715c6d3f334154c9_27fd17d6.displayName = "Bare";

export const Cond_comp_07d5dc8a588fe00b6e132a7f3e0fac98_27fd17d6 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        (!((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.users_error_rx_state_?.valueOf?.() === ""?.valueOf?.()))?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_07d5dc8a588fe00b6e132a7f3e0fac98_27fd17d6.displayName = "Cond";

export const Bare_comp_cb37a8689f425d5bed3c47f75740039a_27fd17d6 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.users_notice_rx_state_
    )
});
Bare_comp_cb37a8689f425d5bed3c47f75740039a_27fd17d6.displayName = "Bare";

export const Cond_comp_f9c794480db25ed287eabde4352007cb_27fd17d6 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        (!((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.users_notice_rx_state_?.valueOf?.() === ""?.valueOf?.()))?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_f9c794480db25ed287eabde4352007cb_27fd17d6.displayName = "Cond";

export const Cond_comp_dd7da03d19c34ba0b8acdcafb4dbb78f_27fd17d6 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        (reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.users_loading_rx_state_?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_dd7da03d19c34ba0b8acdcafb4dbb78f_27fd17d6.displayName = "Cond";

export const Bare_comp_d0aa793a2f1e7c08f550b65205893af6_27fd17d6 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        ("Resultados: "+(JSON.stringify(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.users_total_rx_state_)))
    )
});
Bare_comp_d0aa793a2f1e7c08f550b65205893af6_27fd17d6.displayName = "Bare";

export const Foreach_comp_c9ead73d2162bb3da2fde178b181fa6a_27fd17d6 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        Array.prototype.map.call(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.users_rx_state_ ?? [],((user_rx_state_,index_60c5e8437c0b57173b59617def15a9be)=>(jsx("article",{className:"admin-user-row",key:index_60c5e8437c0b57173b59617def15a9be},jsx("div",{className:"admin-user-main"},jsx("div",{},jsx("p",{className:"admin-user-name"},user_rx_state_?.["name"]),jsx("p",{className:"admin-user-username"},("@"+user_rx_state_?.["username"]))),jsx("div",{className:"admin-user-badges"},jsx("span",{className:"admin-user-id"},("ID "+user_rx_state_?.["id"])),jsx("span",{className:"admin-user-role"},user_rx_state_?.["role"]),jsx("span",{className:((user_rx_state_?.["account_status"]?.valueOf?.() === "disabled"?.valueOf?.()) ? "admin-status-disabled" : "admin-status-active")},((user_rx_state_?.["account_status"]?.valueOf?.() === "disabled"?.valueOf?.()) ? "Suspensa" : "Ativa")))),jsx("div",{className:"admin-user-controls"},jsx("div",{className:"admin-user-actions"},jsx("button",{"aria-expanded":(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.user_details_id_rx_state_?.valueOf?.() === user_rx_state_?.["id"]?.valueOf?.()),className:"quiet-button admin-user-details-toggle",onClick:((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___admin____admin_state.toggle_user_details", ({ ["user_id"] : user_rx_state_?.["id"] }), ({  })))], [_e], ({  })))),type:"button"},"Detalhes"),jsx("button",{className:((user_rx_state_?.["account_status"]?.valueOf?.() === "disabled"?.valueOf?.()) ? "quiet-button admin-user-activate" : "quiet-button admin-user-disable"),onClick:((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___admin____admin_state.open_user_status_dialog", ({ ["user_id"] : user_rx_state_?.["id"], ["status"] : ((user_rx_state_?.["account_status"]?.valueOf?.() === "disabled"?.valueOf?.()) ? "active" : "disabled") }), ({  })))], [_e], ({  })))),type:"button"},((user_rx_state_?.["account_status"]?.valueOf?.() === "disabled"?.valueOf?.()) ? "Reativar" : "Suspender"))),jsx(Fragment,{},((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.user_details_id_rx_state_?.valueOf?.() === user_rx_state_?.["id"]?.valueOf?.())?(jsx(Fragment,{},jsx("div",{className:"admin-user-details"},jsx("span",{},("Identificador: "+user_rx_state_?.["id"])),jsx("span",{},("Criada em: "+(!((user_rx_state_?.["created_at"]?.valueOf?.() === ""?.valueOf?.())) ? user_rx_state_?.["created_at"] : "N\u00e3o informado"))),jsx("span",{},("Papel: "+user_rx_state_?.["role"])),jsx("span",{},("Acesso: "+((user_rx_state_?.["account_status"]?.valueOf?.() === "disabled"?.valueOf?.()) ? "Suspenso" : "Ativo")))))):(jsx(Fragment,{},)))))))))
    )
});
Foreach_comp_c9ead73d2162bb3da2fde178b181fa6a_27fd17d6.displayName = "Foreach";

export const Button_button_b089d8dc3df54b1615505c9942ca9cf7_27fd17d6 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)
const on_click_a3503b478e3fca2f37d1bf2201e7ad27 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___admin____admin_state.change_users_page", ({ ["page"] : (reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.users_page_rx_state_ - 1) }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent, reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state])



    return(
        jsx("button",{className:"quiet-button",disabled:(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.users_page_rx_state_ <= 1),onClick:on_click_a3503b478e3fca2f37d1bf2201e7ad27,type:"button"},children)
    )
});
Button_button_b089d8dc3df54b1615505c9942ca9cf7_27fd17d6.displayName = "Button";

export const Bare_comp_ecb5bcc24db6caa83a9db4eaa642f29e_27fd17d6 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        ("P\u00e1gina "+(JSON.stringify(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.users_page_rx_state_)))
    )
});
Bare_comp_ecb5bcc24db6caa83a9db4eaa642f29e_27fd17d6.displayName = "Bare";

export const Button_button_e4269d5da4e1f592e654b23f795db4d3_27fd17d6 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)
const on_click_e38962c796851825795250e945854d55 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___admin____admin_state.change_users_page", ({ ["page"] : reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.users_next_page_rx_state_ }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent, reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state])



    return(
        jsx("button",{className:"quiet-button",disabled:(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.users_next_page_rx_state_?.valueOf?.() === 0?.valueOf?.()),onClick:on_click_e38962c796851825795250e945854d55,type:"button"},children)
    )
});
Button_button_e4269d5da4e1f592e654b23f795db4d3_27fd17d6.displayName = "Button";

export const Cond_comp_3aaf77cf65972456a7f365b28488d946_27fd17d6 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        (!((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.users_query_rx_state_?.valueOf?.() === ""?.valueOf?.()))?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_3aaf77cf65972456a7f365b28488d946_27fd17d6.displayName = "Cond";

export const Cond_comp_c3a0b82b63c22d4f6cb44da46b458601_27fd17d6 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        ((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.users_rx_state_.length > 0)?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_c3a0b82b63c22d4f6cb44da46b458601_27fd17d6.displayName = "Cond";

export const Bare_comp_44a3d1d32d32a68e780bda8c9609c701_27fd17d6 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        ((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.user_action_status_rx_state_?.valueOf?.() === "disabled"?.valueOf?.()) ? "Suspender conta?" : "Reativar conta?")
    )
});
Bare_comp_44a3d1d32d32a68e780bda8c9609c701_27fd17d6.displayName = "Bare";

export const Bare_comp_1f085553c92a48240a104859aecae011_27fd17d6 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        ((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.user_action_status_rx_state_?.valueOf?.() === "disabled"?.valueOf?.()) ? "A pessoa deixar\u00e1 de acessar as opera\u00e7\u00f5es protegidas at\u00e9 ser reativada." : "A pessoa poder\u00e1 voltar a acessar a conta ap\u00f3s a pr\u00f3xima autentica\u00e7\u00e3o.")
    )
});
Bare_comp_1f085553c92a48240a104859aecae011_27fd17d6.displayName = "Bare";

export const Textarea_textarea_5b199c74f073ed7835046e2b70ce8149_27fd17d6 = memo(({children}) => {
    const ref_admin_user_action_reason = useRef(null); refs["ref_admin_user_action_reason"] = ref_admin_user_action_reason;
const on_change_14c34dd561895ec606b8bfed84440fdd = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___admin____admin_state.set_user_action_reason", ({ ["value"] : _e?.["target"]?.["value"] }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])
const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        jsx("textarea",{className:"admin-user-reason",id:"admin-user-action-reason",maxLength:500,onChange:on_change_14c34dd561895ec606b8bfed84440fdd,ref:ref_admin_user_action_reason,value:reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.user_action_reason_rx_state_},)
    )
});
Textarea_textarea_5b199c74f073ed7835046e2b70ce8149_27fd17d6.displayName = "Textarea";

export const Button_button_e5095f78dfc24925c85a39e7bc9530b3_27fd17d6 = memo(({children}) => {
    const on_click_0d26fd5ed0d84d0906480ace8a132ee9 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___admin____admin_state.close_user_status_dialog", ({  }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])
const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        jsx("button",{className:"quiet-button",disabled:reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.user_action_loading_rx_state_,onClick:on_click_0d26fd5ed0d84d0906480ace8a132ee9,type:"button"},children)
    )
});
Button_button_e5095f78dfc24925c85a39e7bc9530b3_27fd17d6.displayName = "Button";

export const Bare_comp_7e51b515d66b88ecf8102aa0d4f8c798_27fd17d6 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        (reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.user_action_loading_rx_state_ ? "Salvando\u2026" : "Confirmar")
    )
});
Bare_comp_7e51b515d66b88ecf8102aa0d4f8c798_27fd17d6.displayName = "Bare";

export const Button_button_ab3c74b54f69abccfb4810f3d9c83d7e_27fd17d6 = memo(({children}) => {
    const on_click_1f1442115bcb17e15be27e41626a80da = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___admin____admin_state.confirm_user_status_change", ({  }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])
const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        jsx("button",{className:((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.user_action_status_rx_state_?.valueOf?.() === "disabled"?.valueOf?.()) ? "admin-dialog-confirm-danger" : "admin-dialog-confirm"),disabled:reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.user_action_loading_rx_state_,onClick:on_click_1f1442115bcb17e15be27e41626a80da,type:"button"},children)
    )
});
Button_button_ab3c74b54f69abccfb4810f3d9c83d7e_27fd17d6.displayName = "Button";

export const Cond_comp_139461768f8bcf7a32085fdb84652030_27fd17d6 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        (!((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.user_action_id_rx_state_?.valueOf?.() === ""?.valueOf?.()))?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_139461768f8bcf7a32085fdb84652030_27fd17d6.displayName = "Cond";

export const Select_select_b2d66985fcc9ce16f54f6c9c90e26d6a_27fd17d6 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        jsx("select",{className:"admin-search-select",defaultValue:reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.reports_status_filter_rx_state_,name:"status"},children)
    )
});
Select_select_b2d66985fcc9ce16f54f6c9c90e26d6a_27fd17d6.displayName = "Select";

export const Select_select_427c53a0b358117ea4815f27af16ee16_27fd17d6 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        jsx("select",{className:"admin-search-select",defaultValue:reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.reports_type_filter_rx_state_,name:"target_type"},children)
    )
});
Select_select_427c53a0b358117ea4815f27af16ee16_27fd17d6.displayName = "Select";

export const Select_select_739641579fb38d5fc9c2a89b07f9614c_27fd17d6 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        jsx("select",{className:"admin-search-select",defaultValue:reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.reports_reason_filter_rx_state_,name:"reason"},children)
    )
});
Select_select_739641579fb38d5fc9c2a89b07f9614c_27fd17d6.displayName = "Select";

export const Button_button_eaed21e8d2ac0ccf3c94e616e490c418_27fd17d6 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        jsx("button",{className:"admin-search-submit",disabled:reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.reports_loading_rx_state_,type:"submit"},children)
    )
});
Button_button_eaed21e8d2ac0ccf3c94e616e490c418_27fd17d6.displayName = "Button";

export const Form_form_de8445bb7800cf116aa0825d1c96ecf9_27fd17d6 = memo(({children}) => {
    

    const handleSubmit_48691e242a4b959c2231dd9364c97c52 = useCallback((ev) => {
        const $form = ev.target
        ev.preventDefault()
        const form_data = {...Object.fromEntries(new FormData($form).entries()), ...({  })};

        (((...args) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___admin____admin_state.search_reports", ({ ["form"] : form_data }), ({  })))], args, ({  }))))(ev));

        if (false) {
            $form.reset()
        }
    })
    


    return(
        jsx("form",{className:"admin-users-search",onSubmit:handleSubmit_48691e242a4b959c2231dd9364c97c52},children)
    )
});
Form_form_de8445bb7800cf116aa0825d1c96ecf9_27fd17d6.displayName = "Form";

export const Bare_comp_58fa70f2a663ef37b3aabee8c0fce077_27fd17d6 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.reports_error_rx_state_
    )
});
Bare_comp_58fa70f2a663ef37b3aabee8c0fce077_27fd17d6.displayName = "Bare";

export const Cond_comp_2405302ee3b5a8d838b5a1d75921e195_27fd17d6 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        (!((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.reports_error_rx_state_?.valueOf?.() === ""?.valueOf?.()))?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_2405302ee3b5a8d838b5a1d75921e195_27fd17d6.displayName = "Cond";

export const Bare_comp_245f42e2df0e0eb60680e6ae8ab74e22_27fd17d6 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.reports_notice_rx_state_
    )
});
Bare_comp_245f42e2df0e0eb60680e6ae8ab74e22_27fd17d6.displayName = "Bare";

export const Cond_comp_e7721e806db35b9c15c039ec27c9cd1f_27fd17d6 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        (!((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.reports_notice_rx_state_?.valueOf?.() === ""?.valueOf?.()))?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_e7721e806db35b9c15c039ec27c9cd1f_27fd17d6.displayName = "Cond";

export const Cond_comp_9941dd2d7bacf2f703c84763ec9aa233_27fd17d6 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        (reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.reports_loading_rx_state_?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_9941dd2d7bacf2f703c84763ec9aa233_27fd17d6.displayName = "Cond";

export const Bare_comp_d47ac4573baa1c88685a6d9f5d45857f_27fd17d6 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        ("Resultados: "+(JSON.stringify(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.reports_total_rx_state_)))
    )
});
Bare_comp_d47ac4573baa1c88685a6d9f5d45857f_27fd17d6.displayName = "Bare";

export const Foreach_comp_77f975ce2673af4ddf32b96455f87c82_27fd17d6 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        Array.prototype.map.call(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.reports_rx_state_ ?? [],((report_rx_state_,index_303c9c81b27c799106bb977c57771fc1)=>(jsx("article",{className:"admin-report-card",key:index_303c9c81b27c799106bb977c57771fc1},jsx("div",{className:"admin-report-heading"},jsx("div",{className:"admin-report-header-copy"},jsx("p",{className:"admin-user-name"},("Report #"+report_rx_state_?.["id"])),jsx("p",{className:"admin-user-username"},((((("Alvo: "+report_rx_state_?.["target_type"])+" #")+report_rx_state_?.["target_id"])+" \u00b7 Denunciante #")+report_rx_state_?.["reporter_user_id"]))),jsx("span",{className:"admin-user-role"},report_rx_state_?.["status"])),jsx("div",{className:"admin-report-copy"},jsx("p",{className:"admin-report-reason"},("Motivo: "+report_rx_state_?.["reason"])),jsx(Fragment,{},(!((report_rx_state_?.["description"]?.valueOf?.() === ""?.valueOf?.()))?(jsx(Fragment,{},jsx("p",{className:"admin-report-description"},report_rx_state_?.["description"]))):(jsx(Fragment,{},)))),jsx(Fragment,{},(!((report_rx_state_?.["target_snapshot"]?.valueOf?.() === ""?.valueOf?.()))?(jsx(Fragment,{},jsx("details",{className:"admin-report-context"},jsx("summary",{},"Contexto salvo no envio do report"),jsx("pre",{className:"admin-report-snapshot"},report_rx_state_?.["target_snapshot"])))):(jsx(Fragment,{},jsx("p",{className:"admin-report-description"},"Sem snapshot dispon\u00edvel."))))),jsx(Fragment,{},(!((report_rx_state_?.["decision"]?.valueOf?.() === ""?.valueOf?.()))?(jsx(Fragment,{},jsx("p",{className:"admin-report-decision"},("Decis\u00e3o registrada: "+report_rx_state_?.["decision"])))):(jsx(Fragment,{},))))),jsx("div",{className:"admin-report-actions"},jsx("button",{className:"quiet-button",disabled:reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.reports_loading_rx_state_,onClick:((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___admin____admin_state.open_report_review", ({ ["report_id"] : report_rx_state_?.["id"], ["status"] : "reviewing" }), ({  })))], [_e], ({  })))),type:"button"},"Em an\u00e1lise"),jsx("button",{className:"admin-dialog-confirm",disabled:reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.reports_loading_rx_state_,onClick:((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___admin____admin_state.open_report_review", ({ ["report_id"] : report_rx_state_?.["id"], ["status"] : "resolved" }), ({  })))], [_e], ({  })))),type:"button"},"Resolver"),jsx("button",{className:"admin-dialog-confirm-danger",disabled:reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.reports_loading_rx_state_,onClick:((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___admin____admin_state.open_report_review", ({ ["report_id"] : report_rx_state_?.["id"], ["status"] : "rejected" }), ({  })))], [_e], ({  })))),type:"button"},"Rejeitar"))))))
    )
});
Foreach_comp_77f975ce2673af4ddf32b96455f87c82_27fd17d6.displayName = "Foreach";

export const Button_button_1154285649b30834940730606b1854ad_27fd17d6 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)
const on_click_c268673c11e9d9d3223f0998054abf15 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___admin____admin_state.change_reports_page", ({ ["page"] : (reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.reports_page_rx_state_ - 1) }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent, reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state])



    return(
        jsx("button",{className:"quiet-button",disabled:(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.reports_page_rx_state_ <= 1),onClick:on_click_c268673c11e9d9d3223f0998054abf15,type:"button"},children)
    )
});
Button_button_1154285649b30834940730606b1854ad_27fd17d6.displayName = "Button";

export const Bare_comp_bb36e3ffb2067d29582cabe5f0e1b425_27fd17d6 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        ("P\u00e1gina "+(JSON.stringify(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.reports_page_rx_state_)))
    )
});
Bare_comp_bb36e3ffb2067d29582cabe5f0e1b425_27fd17d6.displayName = "Bare";

export const Button_button_a24281ceeb7d9b8b5610787722d07f6f_27fd17d6 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)
const on_click_4a1127c719a3f542185464c18efd6a62 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___admin____admin_state.change_reports_page", ({ ["page"] : reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.reports_next_page_rx_state_ }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent, reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state])



    return(
        jsx("button",{className:"quiet-button",disabled:(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.reports_next_page_rx_state_?.valueOf?.() === 0?.valueOf?.()),onClick:on_click_4a1127c719a3f542185464c18efd6a62,type:"button"},children)
    )
});
Button_button_a24281ceeb7d9b8b5610787722d07f6f_27fd17d6.displayName = "Button";

export const Cond_comp_0435e2318ec54bdfda0fb9231956bbb5_27fd17d6 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        ((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.reports_rx_state_.length > 0)?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_0435e2318ec54bdfda0fb9231956bbb5_27fd17d6.displayName = "Cond";

export const Bare_comp_88b108835be96d34649bea1550fa085e_27fd17d6 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        ((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.report_review_status_rx_state_?.valueOf?.() === "reviewing"?.valueOf?.()) ? "Iniciar an\u00e1lise?" : ((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.report_review_status_rx_state_?.valueOf?.() === "resolved"?.valueOf?.()) ? "Resolver report?" : "Rejeitar report?"))
    )
});
Bare_comp_88b108835be96d34649bea1550fa085e_27fd17d6.displayName = "Bare";

export const Textarea_textarea_436a96c6194c6a50e551cf5f1a8636e0_27fd17d6 = memo(({children}) => {
    const ref_admin_report_decision = useRef(null); refs["ref_admin_report_decision"] = ref_admin_report_decision;
const on_change_5457a888ed31779bfddcd073e12dbf64 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___admin____admin_state.set_report_review_decision", ({ ["value"] : _e?.["target"]?.["value"] }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])
const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        jsx("textarea",{className:"admin-user-reason",id:"admin-report-decision",maxLength:2000,onChange:on_change_5457a888ed31779bfddcd073e12dbf64,ref:ref_admin_report_decision,value:reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.report_review_decision_rx_state_},)
    )
});
Textarea_textarea_436a96c6194c6a50e551cf5f1a8636e0_27fd17d6.displayName = "Textarea";

export const Button_button_384b667f4511d6f23815eb621c3ce895_27fd17d6 = memo(({children}) => {
    const on_click_5c673a2c321234f0fba756ce519a67ef = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___admin____admin_state.close_report_review", ({  }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])
const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        jsx("button",{className:"quiet-button",disabled:reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.report_review_loading_rx_state_,onClick:on_click_5c673a2c321234f0fba756ce519a67ef,type:"button"},children)
    )
});
Button_button_384b667f4511d6f23815eb621c3ce895_27fd17d6.displayName = "Button";

export const Bare_comp_d1223676b1ea82e90b55b2a327e1f6d2_27fd17d6 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        (reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.report_review_loading_rx_state_ ? "Salvando\u2026" : "Confirmar decis\u00e3o")
    )
});
Bare_comp_d1223676b1ea82e90b55b2a327e1f6d2_27fd17d6.displayName = "Bare";

export const Button_button_34d8e150f8b119a944f372e1427fbb55_27fd17d6 = memo(({children}) => {
    const on_click_ea3cc53ce1e7a0717e1276db0982d3b9 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___admin____admin_state.save_report_review", ({  }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])
const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        jsx("button",{className:"admin-dialog-confirm",disabled:reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.report_review_loading_rx_state_,onClick:on_click_ea3cc53ce1e7a0717e1276db0982d3b9,type:"button"},children)
    )
});
Button_button_34d8e150f8b119a944f372e1427fbb55_27fd17d6.displayName = "Button";

export const Cond_comp_fa41ed9fdfa8236c96e3bf63635b2f21_27fd17d6 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        (!((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.report_review_id_rx_state_?.valueOf?.() === ""?.valueOf?.()))?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_fa41ed9fdfa8236c96e3bf63635b2f21_27fd17d6.displayName = "Cond";
