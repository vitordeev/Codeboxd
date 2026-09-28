
import {ReflexEvent,applyEventActions,getRefValue,getRefValues,isTrue,refs} from "$/utils/state"
import {StateContexts,addEvents} from "$/utils/context"
import {Fragment,memo,useCallback,useContext,useEffect} from "react"
import {jsx} from "@emotion/react"








export const Bare_comp_bd554523900b9b74daaac23eac57e50a_b4177684 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state)



    return(
        reflex___state____state__codeboxd_main___state___session____session_state.error_message_rx_state_
    )
});
Bare_comp_bd554523900b9b74daaac23eac57e50a_b4177684.displayName = "Bare";

export const Cond_comp_d2b0fe9982d8d79ffc1f395127db034c_b4177684 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state)



    return(
        (!((reflex___state____state__codeboxd_main___state___session____session_state.error_message_rx_state_?.valueOf?.() === ""?.valueOf?.()))?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_d2b0fe9982d8d79ffc1f395127db034c_b4177684.displayName = "Cond";

export const Bare_comp_bc788da7e24e9bf92fef2fd1b3b1409e_b4177684 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state)



    return(
        (reflex___state____state__codeboxd_main___state___session____session_state.is_loading_rx_state_ ? "Entrando..." : "Entrar")
    )
});
Bare_comp_bc788da7e24e9bf92fef2fd1b3b1409e_b4177684.displayName = "Bare";

export const Button_button_8e95c49230a93b1b2c7eb23627d3a910_b4177684 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state)



    return(
        jsx("button",{className:"w-full h-12 bg-[#F5B300] hover:bg-[#e0a400] text-black font-semibold text-[14px] rounded-xl flex items-center justify-center gap-2 transition-colors duration-150 active:scale-[0.99] shadow-sm",disabled:reflex___state____state__codeboxd_main___state___session____session_state.is_loading_rx_state_,type:"submit"},children)
    )
});
Button_button_8e95c49230a93b1b2c7eb23627d3a910_b4177684.displayName = "Button";

export const Form_form_c6f3206e1a277c3649676bb54018c5d7_b4177684 = memo(({children}) => {
    

    const handleSubmit_c2845fdb739a80389632594cf4229ad7 = useCallback((ev) => {
        const $form = ev.target
        ev.preventDefault()
        const form_data = {...Object.fromEntries(new FormData($form).entries()), ...({ ["email"] : getRefValue(refs["ref_email"]), ["password"] : getRefValue(refs["ref_password"]) })};

        (((...args) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.login", ({ ["form"] : form_data }), ({  })))], args, ({  }))))(ev));

        if (false) {
            $form.reset()
        }
    })
    


    return(
        jsx("form",{className:"space-y-5",onSubmit:handleSubmit_c2845fdb739a80389632594cf4229ad7},children)
    )
});
Form_form_c6f3206e1a277c3649676bb54018c5d7_b4177684.displayName = "Form";
