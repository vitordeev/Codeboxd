
import {ReflexEvent,applyEventActions,getRefValue,getRefValues,isTrue,refs} from "$/utils/state"
import {StateContexts,addEvents} from "$/utils/context"
import {Fragment,memo,useCallback,useContext,useEffect} from "react"
import {jsx} from "@emotion/react"








export const Bare_comp_bd554523900b9b74daaac23eac57e50a_24663de3 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state)



    return(
        reflex___state____state__codeboxd_main___state___session____session_state.error_message_rx_state_
    )
});
Bare_comp_bd554523900b9b74daaac23eac57e50a_24663de3.displayName = "Bare";

export const Cond_comp_d2b0fe9982d8d79ffc1f395127db034c_24663de3 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state)



    return(
        (!((reflex___state____state__codeboxd_main___state___session____session_state.error_message_rx_state_?.valueOf?.() === ""?.valueOf?.()))?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_d2b0fe9982d8d79ffc1f395127db034c_24663de3.displayName = "Cond";

export const Bare_comp_a6beb1f4af3b3df9eabca8f297bbff91_24663de3 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state)



    return(
        (reflex___state____state__codeboxd_main___state___session____session_state.is_loading_rx_state_ ? "Criando conta\u2026" : "Criar conta")
    )
});
Bare_comp_a6beb1f4af3b3df9eabca8f297bbff91_24663de3.displayName = "Bare";

export const Button_button_5b6e6dfc979f83b3bf301c2a7d95ee04_24663de3 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state)



    return(
        jsx("button",{className:"w-full h-12 rounded-xl bg-[#F5B300] text-black font-semibold",disabled:reflex___state____state__codeboxd_main___state___session____session_state.is_loading_rx_state_,type:"submit"},children)
    )
});
Button_button_5b6e6dfc979f83b3bf301c2a7d95ee04_24663de3.displayName = "Button";

export const Form_form_e182775e5e3a7c3d7997d91a7810b186_24663de3 = memo(({children}) => {
    

    const handleSubmit_243dd4d989efc4e86fa0963665c03f64 = useCallback((ev) => {
        const $form = ev.target
        ev.preventDefault()
        const form_data = {...Object.fromEntries(new FormData($form).entries()), ...({ ["name"] : getRefValue(refs["ref_name"]), ["username"] : getRefValue(refs["ref_username"]), ["email"] : getRefValue(refs["ref_email"]), ["password"] : getRefValue(refs["ref_password"]), ["confirm_password"] : getRefValue(refs["ref_confirm_password"]) })};

        (((...args) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.signup", ({ ["form"] : form_data }), ({  })))], args, ({  }))))(ev));

        if (false) {
            $form.reset()
        }
    })
    


    return(
        jsx("form",{className:"space-y-4",onSubmit:handleSubmit_243dd4d989efc4e86fa0963665c03f64},children)
    )
});
Form_form_e182775e5e3a7c3d7997d91a7810b186_24663de3.displayName = "Form";

export const Bare_comp_a5d80918295bad0d50c023c3fc96a50f_24663de3 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state)



    return(
        (reflex___state____state__codeboxd_main___state___session____session_state.is_loading_rx_state_ ? "Enviando\u2026" : "Enviar c\u00f3digo por e-mail")
    )
});
Bare_comp_a5d80918295bad0d50c023c3fc96a50f_24663de3.displayName = "Bare";

export const Button_button_9c5acebbe5645f76ea77f59a36c4214d_24663de3 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state)



    return(
        jsx("button",{className:"action-button reset-primary-button",disabled:reflex___state____state__codeboxd_main___state___session____session_state.is_loading_rx_state_,type:"submit"},children)
    )
});
Button_button_9c5acebbe5645f76ea77f59a36c4214d_24663de3.displayName = "Button";

export const Form_form_c4800359ac30de6b03e99de0058513c0_24663de3 = memo(({children}) => {
    

    const handleSubmit_cad83e0ade6c6b9574a002cef0b5c8fc = useCallback((ev) => {
        const $form = ev.target
        ev.preventDefault()
        const form_data = {...Object.fromEntries(new FormData($form).entries()), ...({ ["email"] : getRefValue(refs["ref_email"]) })};

        (((...args) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.request_password_reset", ({ ["form"] : form_data }), ({  })))], args, ({  }))))(ev));

        if (false) {
            $form.reset()
        }
    })
    


    return(
        jsx("form",{className:"reset-form",onSubmit:handleSubmit_cad83e0ade6c6b9574a002cef0b5c8fc},children)
    )
});
Form_form_c4800359ac30de6b03e99de0058513c0_24663de3.displayName = "Form";

export const Bare_comp_17d097c4fde87a6e019037ec5ed8d6fc_24663de3 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state)



    return(
        (reflex___state____state__codeboxd_main___state___session____session_state.is_loading_rx_state_ ? "Salvando\u2026" : "Salvar nova senha")
    )
});
Bare_comp_17d097c4fde87a6e019037ec5ed8d6fc_24663de3.displayName = "Bare";

export const Form_form_bdb5309a7be5584730e105a67802ca39_24663de3 = memo(({children}) => {
    

    const handleSubmit_c6787ffaac9ce5acdb254c1ff86611ec = useCallback((ev) => {
        const $form = ev.target
        ev.preventDefault()
        const form_data = {...Object.fromEntries(new FormData($form).entries()), ...({ ["email"] : getRefValue(refs["ref_email"]), ["code"] : getRefValue(refs["ref_code"]), ["password"] : getRefValue(refs["ref_password"]), ["confirm_password"] : getRefValue(refs["ref_confirm_password"]) })};

        (((...args) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.reset_password", ({ ["form"] : form_data }), ({  })))], args, ({  }))))(ev));

        if (false) {
            $form.reset()
        }
    })
    


    return(
        jsx("form",{className:"reset-form",onSubmit:handleSubmit_c6787ffaac9ce5acdb254c1ff86611ec},children)
    )
});
Form_form_bdb5309a7be5584730e105a67802ca39_24663de3.displayName = "Form";

export const Bare_comp_b59e4587ea96f32a2bdd391f7055ad9b_24663de3 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state)



    return(
        reflex___state____state__codeboxd_main___state___session____session_state.reset_message_rx_state_
    )
});
Bare_comp_b59e4587ea96f32a2bdd391f7055ad9b_24663de3.displayName = "Bare";

export const P_p_831c05a2f88ab3fbeb1f758261923844_24663de3 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state)



    return(
        jsx("p",{className:(reflex___state____state__codeboxd_main___state___session____session_state.reset_success_rx_state_ ? "reset-message reset-message-success" : "reset-message reset-message-error"),role:"status"},children)
    )
});
P_p_831c05a2f88ab3fbeb1f758261923844_24663de3.displayName = "P";

export const Cond_comp_708f13b6c2f7fbe600cf28d7796fa90a_24663de3 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state)



    return(
        (!((reflex___state____state__codeboxd_main___state___session____session_state.reset_message_rx_state_?.valueOf?.() === ""?.valueOf?.()))?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_708f13b6c2f7fbe600cf28d7796fa90a_24663de3.displayName = "Cond";
