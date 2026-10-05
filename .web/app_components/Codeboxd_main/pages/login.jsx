
import {ReflexEvent,applyEventActions,getRefValue,getRefValues,isTrue,mergeSlotProps,refs} from "$/utils/state"
import {StateContexts,addEvents} from "$/utils/context"
import {Fragment,memo,useCallback,useContext,useEffect} from "react"
import {jsx} from "@emotion/react"








export const Bare_comp_d6ddc95630766b330eb2ccc495464542_b4177684 = /*#__PURE__*/ (() => {
const Bare_comp_d6ddc95630766b330eb2ccc495464542_b4177684 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state)



    return(
        reflex___state____state__codeboxd_main___state___session____session_state.error_message_rx_state_
    )
});
Bare_comp_d6ddc95630766b330eb2ccc495464542_b4177684.displayName = "Bare";
return Bare_comp_d6ddc95630766b330eb2ccc495464542_b4177684;
})();

export const Cond_comp_d0da96d081f6234401b69e992074904a_b4177684 = /*#__PURE__*/ (() => {
const Cond_comp_d0da96d081f6234401b69e992074904a_b4177684 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state)



    return(
        (!((reflex___state____state__codeboxd_main___state___session____session_state.error_message_rx_state_?.valueOf?.() === ""?.valueOf?.()))?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_d0da96d081f6234401b69e992074904a_b4177684.displayName = "Cond";
return Cond_comp_d0da96d081f6234401b69e992074904a_b4177684;
})();

export const Bare_comp_06be5253faecf12c51c458013f1e93db_b4177684 = /*#__PURE__*/ (() => {
const Bare_comp_06be5253faecf12c51c458013f1e93db_b4177684 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state)



    return(
        (reflex___state____state__codeboxd_main___state___session____session_state.is_loading_rx_state_ ? "Entrando..." : "Entrar")
    )
});
Bare_comp_06be5253faecf12c51c458013f1e93db_b4177684.displayName = "Bare";
return Bare_comp_06be5253faecf12c51c458013f1e93db_b4177684;
})();

export const Button_button_ab9254a15f779b31bcc9fd987038a15d_b4177684 = /*#__PURE__*/ (() => {
const Button_button_ab9254a15f779b31bcc9fd987038a15d_b4177684 = memo(({children, ...rest}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state)



    return(
        jsx("button",{...mergeSlotProps(rest, ({ className:"w-full h-12 bg-[#F5B300] hover:bg-[#e0a400] text-black font-semibold text-[14px] rounded-xl flex items-center justify-center gap-2 transition-colors duration-150 active:scale-[0.99] shadow-sm", disabled:reflex___state____state__codeboxd_main___state___session____session_state.is_loading_rx_state_, type:"submit" }))},children)
    )
});
Button_button_ab9254a15f779b31bcc9fd987038a15d_b4177684.displayName = "Button";
return Button_button_ab9254a15f779b31bcc9fd987038a15d_b4177684;
})();

export const Form_form_745ef7aea39e455da8df071194c5d757_b4177684 = /*#__PURE__*/ (() => {
const Form_form_745ef7aea39e455da8df071194c5d757_b4177684 = memo(({children, ...rest}) => {
    

    const handleSubmit_6368a5a3a2818c814bf47570087d3019 = useCallback((ev) => {
        const $form = ev.target
        ev.preventDefault()
        const form_data = {...Object.fromEntries(new FormData($form).entries()), ...({ ["email"] : getRefValue(refs["ref_email"]), ["password"] : getRefValue(refs["ref_password"]) })};

        (((...args) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.login", ({ ["form"] : form_data }), ({  })))], args, ({  }))))(ev));

        if (false) {
            $form.reset()
        }
    })
    


    return(
        jsx("form",{...mergeSlotProps(rest, ({ className:"space-y-5", onSubmit:handleSubmit_6368a5a3a2818c814bf47570087d3019 }))},children)
    )
});
Form_form_745ef7aea39e455da8df071194c5d757_b4177684.displayName = "Form";
return Form_form_745ef7aea39e455da8df071194c5d757_b4177684;
})();
