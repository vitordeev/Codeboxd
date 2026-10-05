
import {ReflexEvent,applyEventActions,getRefValue,getRefValues,isTrue,mergeSlotProps,refs} from "$/utils/state"
import {StateContexts,addEvents} from "$/utils/context"
import {Fragment,memo,useCallback,useContext,useEffect} from "react"
import {jsx} from "@emotion/react"








export const Bare_comp_d6ddc95630766b330eb2ccc495464542_24663de3 = /*#__PURE__*/ (() => {
const Bare_comp_d6ddc95630766b330eb2ccc495464542_24663de3 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state)



    return(
        reflex___state____state__codeboxd_main___state___session____session_state.error_message_rx_state_
    )
});
Bare_comp_d6ddc95630766b330eb2ccc495464542_24663de3.displayName = "Bare";
return Bare_comp_d6ddc95630766b330eb2ccc495464542_24663de3;
})();

export const Cond_comp_d0da96d081f6234401b69e992074904a_24663de3 = /*#__PURE__*/ (() => {
const Cond_comp_d0da96d081f6234401b69e992074904a_24663de3 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state)



    return(
        (!((reflex___state____state__codeboxd_main___state___session____session_state.error_message_rx_state_?.valueOf?.() === ""?.valueOf?.()))?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_d0da96d081f6234401b69e992074904a_24663de3.displayName = "Cond";
return Cond_comp_d0da96d081f6234401b69e992074904a_24663de3;
})();

export const Bare_comp_74c3925696748caf399eacc402ccec7d_24663de3 = /*#__PURE__*/ (() => {
const Bare_comp_74c3925696748caf399eacc402ccec7d_24663de3 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state)



    return(
        (reflex___state____state__codeboxd_main___state___session____session_state.is_loading_rx_state_ ? "Criando conta\u2026" : "Criar conta")
    )
});
Bare_comp_74c3925696748caf399eacc402ccec7d_24663de3.displayName = "Bare";
return Bare_comp_74c3925696748caf399eacc402ccec7d_24663de3;
})();

export const Button_button_6121de223ccfd37a1dd51ccba7e9901a_24663de3 = /*#__PURE__*/ (() => {
const Button_button_6121de223ccfd37a1dd51ccba7e9901a_24663de3 = memo(({children, ...rest}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state)



    return(
        jsx("button",{...mergeSlotProps(rest, ({ className:"w-full h-12 rounded-xl bg-[#F5B300] text-black font-semibold", disabled:reflex___state____state__codeboxd_main___state___session____session_state.is_loading_rx_state_, type:"submit" }))},children)
    )
});
Button_button_6121de223ccfd37a1dd51ccba7e9901a_24663de3.displayName = "Button";
return Button_button_6121de223ccfd37a1dd51ccba7e9901a_24663de3;
})();

export const Form_form_0d63a0582c47089970dce39beb90a70c_24663de3 = /*#__PURE__*/ (() => {
const Form_form_0d63a0582c47089970dce39beb90a70c_24663de3 = memo(({children, ...rest}) => {
    

    const handleSubmit_a5cdb3228b40e37440cc5a580c9b7a3d = useCallback((ev) => {
        const $form = ev.target
        ev.preventDefault()
        const form_data = {...Object.fromEntries(new FormData($form).entries()), ...({ ["name"] : getRefValue(refs["ref_name"]), ["username"] : getRefValue(refs["ref_username"]), ["email"] : getRefValue(refs["ref_email"]), ["password"] : getRefValue(refs["ref_password"]), ["confirm_password"] : getRefValue(refs["ref_confirm_password"]) })};

        (((...args) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.signup", ({ ["form"] : form_data }), ({  })))], args, ({  }))))(ev));

        if (false) {
            $form.reset()
        }
    })
    


    return(
        jsx("form",{...mergeSlotProps(rest, ({ className:"space-y-4", onSubmit:handleSubmit_a5cdb3228b40e37440cc5a580c9b7a3d }))},children)
    )
});
Form_form_0d63a0582c47089970dce39beb90a70c_24663de3.displayName = "Form";
return Form_form_0d63a0582c47089970dce39beb90a70c_24663de3;
})();

export const Bare_comp_03cb61018bd519309e056a44c3ae5bf6_24663de3 = /*#__PURE__*/ (() => {
const Bare_comp_03cb61018bd519309e056a44c3ae5bf6_24663de3 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state)



    return(
        (reflex___state____state__codeboxd_main___state___session____session_state.is_loading_rx_state_ ? "Enviando\u2026" : "Enviar c\u00f3digo por e-mail")
    )
});
Bare_comp_03cb61018bd519309e056a44c3ae5bf6_24663de3.displayName = "Bare";
return Bare_comp_03cb61018bd519309e056a44c3ae5bf6_24663de3;
})();

export const Button_button_3d1089ca679c8890bb345aeaae4a6a9f_24663de3 = /*#__PURE__*/ (() => {
const Button_button_3d1089ca679c8890bb345aeaae4a6a9f_24663de3 = memo(({children, ...rest}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state)



    return(
        jsx("button",{...mergeSlotProps(rest, ({ className:"action-button reset-primary-button", disabled:reflex___state____state__codeboxd_main___state___session____session_state.is_loading_rx_state_, type:"submit" }))},children)
    )
});
Button_button_3d1089ca679c8890bb345aeaae4a6a9f_24663de3.displayName = "Button";
return Button_button_3d1089ca679c8890bb345aeaae4a6a9f_24663de3;
})();

export const Form_form_552394eb9fc973183a3925032a285ed2_24663de3 = /*#__PURE__*/ (() => {
const Form_form_552394eb9fc973183a3925032a285ed2_24663de3 = memo(({children, ...rest}) => {
    

    const handleSubmit_c71fc3035595e2dad933518a6f79ddcc = useCallback((ev) => {
        const $form = ev.target
        ev.preventDefault()
        const form_data = {...Object.fromEntries(new FormData($form).entries()), ...({ ["email"] : getRefValue(refs["ref_email"]) })};

        (((...args) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.request_password_reset", ({ ["form"] : form_data }), ({  })))], args, ({  }))))(ev));

        if (false) {
            $form.reset()
        }
    })
    


    return(
        jsx("form",{...mergeSlotProps(rest, ({ className:"reset-form", onSubmit:handleSubmit_c71fc3035595e2dad933518a6f79ddcc }))},children)
    )
});
Form_form_552394eb9fc973183a3925032a285ed2_24663de3.displayName = "Form";
return Form_form_552394eb9fc973183a3925032a285ed2_24663de3;
})();

export const Bare_comp_6e70e18b8ff094d45b3dfce3bd40a68f_24663de3 = /*#__PURE__*/ (() => {
const Bare_comp_6e70e18b8ff094d45b3dfce3bd40a68f_24663de3 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state)



    return(
        (reflex___state____state__codeboxd_main___state___session____session_state.is_loading_rx_state_ ? "Salvando\u2026" : "Salvar nova senha")
    )
});
Bare_comp_6e70e18b8ff094d45b3dfce3bd40a68f_24663de3.displayName = "Bare";
return Bare_comp_6e70e18b8ff094d45b3dfce3bd40a68f_24663de3;
})();

export const Form_form_35c0db9690f8e9d13159d1c471b3c621_24663de3 = /*#__PURE__*/ (() => {
const Form_form_35c0db9690f8e9d13159d1c471b3c621_24663de3 = memo(({children, ...rest}) => {
    

    const handleSubmit_1b3e7830195c5e213fac48b353275913 = useCallback((ev) => {
        const $form = ev.target
        ev.preventDefault()
        const form_data = {...Object.fromEntries(new FormData($form).entries()), ...({ ["email"] : getRefValue(refs["ref_email"]), ["code"] : getRefValue(refs["ref_code"]), ["password"] : getRefValue(refs["ref_password"]), ["confirm_password"] : getRefValue(refs["ref_confirm_password"]) })};

        (((...args) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.reset_password", ({ ["form"] : form_data }), ({  })))], args, ({  }))))(ev));

        if (false) {
            $form.reset()
        }
    })
    


    return(
        jsx("form",{...mergeSlotProps(rest, ({ className:"reset-form", onSubmit:handleSubmit_1b3e7830195c5e213fac48b353275913 }))},children)
    )
});
Form_form_35c0db9690f8e9d13159d1c471b3c621_24663de3.displayName = "Form";
return Form_form_35c0db9690f8e9d13159d1c471b3c621_24663de3;
})();

export const Bare_comp_1f5d009495803832abd50a986278ad37_24663de3 = /*#__PURE__*/ (() => {
const Bare_comp_1f5d009495803832abd50a986278ad37_24663de3 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state)



    return(
        reflex___state____state__codeboxd_main___state___session____session_state.reset_message_rx_state_
    )
});
Bare_comp_1f5d009495803832abd50a986278ad37_24663de3.displayName = "Bare";
return Bare_comp_1f5d009495803832abd50a986278ad37_24663de3;
})();

export const P_p_7feab365a74248fcf5af91f995730ce6_24663de3 = /*#__PURE__*/ (() => {
const P_p_7feab365a74248fcf5af91f995730ce6_24663de3 = memo(({children, ...rest}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state)



    return(
        jsx("p",{...mergeSlotProps(rest, ({ className:(reflex___state____state__codeboxd_main___state___session____session_state.reset_success_rx_state_ ? "reset-message reset-message-success" : "reset-message reset-message-error"), role:"status" }))},children)
    )
});
P_p_7feab365a74248fcf5af91f995730ce6_24663de3.displayName = "P";
return P_p_7feab365a74248fcf5af91f995730ce6_24663de3;
})();

export const Cond_comp_4d8bd650916c29726eafaba30e66fc08_24663de3 = /*#__PURE__*/ (() => {
const Cond_comp_4d8bd650916c29726eafaba30e66fc08_24663de3 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state)



    return(
        (!((reflex___state____state__codeboxd_main___state___session____session_state.reset_message_rx_state_?.valueOf?.() === ""?.valueOf?.()))?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_4d8bd650916c29726eafaba30e66fc08_24663de3.displayName = "Cond";
return Cond_comp_4d8bd650916c29726eafaba30e66fc08_24663de3;
})();
