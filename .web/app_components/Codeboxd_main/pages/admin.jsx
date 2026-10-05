
import {ReflexEvent,applyEventActions,getRefValue,getRefValues,isTrue,mergeSlotProps,refs} from "$/utils/state"
import {Fragment,memo,useCallback,useContext,useEffect,useRef} from "react"
import {StateContexts,addEvents} from "$/utils/context"
import {jsx} from "@emotion/react"
import {DynamicIcon} from "lucide-react/dynamic.mjs"








export const Input_input_253ef7f5265c0c70e54d5f86133afb44_27fd17d6 = /*#__PURE__*/ (() => {
const Input_input_253ef7f5265c0c70e54d5f86133afb44_27fd17d6 = memo(({children, ...rest}) => {
    const ref_admin_password = useRef(null); refs["ref_admin_password"] = ref_admin_password;
const reflex___state____state__codeboxd_main___state___session____session_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state)



    return(
        jsx("input",{...mergeSlotProps(rest, ({ autoComplete:"current-password", className:"admin-login-input admin-password-input", id:"admin_password", name:"password", placeholder:"Sua senha", ref:ref_admin_password, required:true, type:(reflex___state____state__codeboxd_main___state___session____session_state.admin_password_visible_rx_state_ ? "text" : "password") }))},)
    )
});
Input_input_253ef7f5265c0c70e54d5f86133afb44_27fd17d6.displayName = "Input";
return Input_input_253ef7f5265c0c70e54d5f86133afb44_27fd17d6;
})();

export const Dynamicicon_dynamicicon_6eafa6f626bbd88a24a1d680a380310a_27fd17d6 = /*#__PURE__*/ (() => {
const Dynamicicon_dynamicicon_6eafa6f626bbd88a24a1d680a380310a_27fd17d6 = memo(({children, ...rest}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state)



    return(
        jsx(DynamicIcon,{...mergeSlotProps(rest, ({ name:(reflex___state____state__codeboxd_main___state___session____session_state.admin_password_visible_rx_state_ ? "eye-off" : "eye").replaceAll("_", "-"), size:18 }))},)
    )
});
Dynamicicon_dynamicicon_6eafa6f626bbd88a24a1d680a380310a_27fd17d6.displayName = "DynamicIcon";
return Dynamicicon_dynamicicon_6eafa6f626bbd88a24a1d680a380310a_27fd17d6;
})();

export const Button_button_5490380b4c4edb2b46411f61fd106a79_27fd17d6 = /*#__PURE__*/ (() => {
const Button_button_5490380b4c4edb2b46411f61fd106a79_27fd17d6 = memo(({children, ...rest}) => {
    const on_click_fa97716112163c9dbf5dad0e92987b4b = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.toggle_admin_password", ({  }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])
const reflex___state____state__codeboxd_main___state___session____session_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state)



    return(
        jsx("button",{...mergeSlotProps(rest, ({ "aria-label":(reflex___state____state__codeboxd_main___state___session____session_state.admin_password_visible_rx_state_ ? "Ocultar senha" : "Mostrar senha"), className:"admin-password-toggle", onClick:on_click_fa97716112163c9dbf5dad0e92987b4b, type:"button" }))},children)
    )
});
Button_button_5490380b4c4edb2b46411f61fd106a79_27fd17d6.displayName = "Button";
return Button_button_5490380b4c4edb2b46411f61fd106a79_27fd17d6;
})();

export const Bare_comp_d6ddc95630766b330eb2ccc495464542_27fd17d6 = /*#__PURE__*/ (() => {
const Bare_comp_d6ddc95630766b330eb2ccc495464542_27fd17d6 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state)



    return(
        reflex___state____state__codeboxd_main___state___session____session_state.error_message_rx_state_
    )
});
Bare_comp_d6ddc95630766b330eb2ccc495464542_27fd17d6.displayName = "Bare";
return Bare_comp_d6ddc95630766b330eb2ccc495464542_27fd17d6;
})();

export const Cond_comp_d0da96d081f6234401b69e992074904a_27fd17d6 = /*#__PURE__*/ (() => {
const Cond_comp_d0da96d081f6234401b69e992074904a_27fd17d6 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state)



    return(
        (!((reflex___state____state__codeboxd_main___state___session____session_state.error_message_rx_state_?.valueOf?.() === ""?.valueOf?.()))?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_d0da96d081f6234401b69e992074904a_27fd17d6.displayName = "Cond";
return Cond_comp_d0da96d081f6234401b69e992074904a_27fd17d6;
})();

export const Bare_comp_25d74a18e5152708f4c1f6e7cb7a8458_27fd17d6 = /*#__PURE__*/ (() => {
const Bare_comp_25d74a18e5152708f4c1f6e7cb7a8458_27fd17d6 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state)



    return(
        (reflex___state____state__codeboxd_main___state___session____session_state.is_loading_rx_state_ ? "Verificando acesso\u2026" : "Entrar na administra\u00e7\u00e3o")
    )
});
Bare_comp_25d74a18e5152708f4c1f6e7cb7a8458_27fd17d6.displayName = "Bare";
return Bare_comp_25d74a18e5152708f4c1f6e7cb7a8458_27fd17d6;
})();

export const Button_button_ed674b22ade1051b7a1c7a57a0733ede_27fd17d6 = /*#__PURE__*/ (() => {
const Button_button_ed674b22ade1051b7a1c7a57a0733ede_27fd17d6 = memo(({children, ...rest}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state)



    return(
        jsx("button",{...mergeSlotProps(rest, ({ className:"admin-login-submit", disabled:reflex___state____state__codeboxd_main___state___session____session_state.is_loading_rx_state_, type:"submit" }))},children)
    )
});
Button_button_ed674b22ade1051b7a1c7a57a0733ede_27fd17d6.displayName = "Button";
return Button_button_ed674b22ade1051b7a1c7a57a0733ede_27fd17d6;
})();

export const Form_form_60efaf3398fceef1e3e061f1a9094b5a_27fd17d6 = /*#__PURE__*/ (() => {
const Form_form_60efaf3398fceef1e3e061f1a9094b5a_27fd17d6 = memo(({children, ...rest}) => {
    

    const handleSubmit_b0505ff19ad06207feb936ceea6bbe7f = useCallback((ev) => {
        const $form = ev.target
        ev.preventDefault()
        const form_data = {...Object.fromEntries(new FormData($form).entries()), ...({ ["admin_email"] : getRefValue(refs["ref_admin_email"]), ["admin_password"] : getRefValue(refs["ref_admin_password"]) })};

        (((...args) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.admin_login", ({ ["form"] : form_data }), ({  })))], args, ({  }))))(ev));

        if (false) {
            $form.reset()
        }
    })
    


    return(
        jsx("form",{...mergeSlotProps(rest, ({ className:"admin-login-form", onSubmit:handleSubmit_b0505ff19ad06207feb936ceea6bbe7f }))},children)
    )
});
Form_form_60efaf3398fceef1e3e061f1a9094b5a_27fd17d6.displayName = "Form";
return Form_form_60efaf3398fceef1e3e061f1a9094b5a_27fd17d6;
})();

export const Button_button_812bd98f23a88229e0770231fd2c7a8b_27fd17d6 = /*#__PURE__*/ (() => {
const Button_button_812bd98f23a88229e0770231fd2c7a8b_27fd17d6 = memo(({children, ...rest}) => {
    const on_click_04fd11fb12f6e03482bf1190dac1510d = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.logout", ({  }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])



    return(
        jsx("button",{...mergeSlotProps(rest, ({ className:"quiet-button admin-logout-button", onClick:on_click_04fd11fb12f6e03482bf1190dac1510d, type:"button" }))},children)
    )
});
Button_button_812bd98f23a88229e0770231fd2c7a8b_27fd17d6.displayName = "Button";
return Button_button_812bd98f23a88229e0770231fd2c7a8b_27fd17d6;
})();

export const Input_input_1bca3dbad26d88db7feb080fd562516c_27fd17d6 = /*#__PURE__*/ (() => {
const Input_input_1bca3dbad26d88db7feb080fd562516c_27fd17d6 = memo(({children, ...rest}) => {
    const ref_admin_user_search = useRef(null); refs["ref_admin_user_search"] = ref_admin_user_search;
const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        jsx("input",{...mergeSlotProps(rest, ({ className:"admin-search-input", defaultValue:reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.users_query_rx_state_, id:"admin-user-search", name:"search", placeholder:"Ex.: nome de usu\u00e1rio ou 123", ref:ref_admin_user_search, required:true, type:"search" }))},)
    )
});
Input_input_1bca3dbad26d88db7feb080fd562516c_27fd17d6.displayName = "Input";
return Input_input_1bca3dbad26d88db7feb080fd562516c_27fd17d6;
})();

export const Select_select_39334773620b560de202bdb2f3cd8b5c_27fd17d6 = /*#__PURE__*/ (() => {
const Select_select_39334773620b560de202bdb2f3cd8b5c_27fd17d6 = memo(({children, ...rest}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        jsx("select",{...mergeSlotProps(rest, ({ className:"admin-search-select", defaultValue:reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.users_status_filter_rx_state_, name:"account_status" }))},children)
    )
});
Select_select_39334773620b560de202bdb2f3cd8b5c_27fd17d6.displayName = "Select";
return Select_select_39334773620b560de202bdb2f3cd8b5c_27fd17d6;
})();

export const Select_select_79049f315f1743029bfebb01ebeeeffb_27fd17d6 = /*#__PURE__*/ (() => {
const Select_select_79049f315f1743029bfebb01ebeeeffb_27fd17d6 = memo(({children, ...rest}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        jsx("select",{...mergeSlotProps(rest, ({ className:"admin-search-select", defaultValue:reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.users_role_filter_rx_state_, name:"role" }))},children)
    )
});
Select_select_79049f315f1743029bfebb01ebeeeffb_27fd17d6.displayName = "Select";
return Select_select_79049f315f1743029bfebb01ebeeeffb_27fd17d6;
})();

export const Bare_comp_e33efca5a9ebb2af5da3a3c69b56c7d1_27fd17d6 = /*#__PURE__*/ (() => {
const Bare_comp_e33efca5a9ebb2af5da3a3c69b56c7d1_27fd17d6 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        (reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.users_loading_rx_state_ ? "Buscando\u2026" : "Pesquisar")
    )
});
Bare_comp_e33efca5a9ebb2af5da3a3c69b56c7d1_27fd17d6.displayName = "Bare";
return Bare_comp_e33efca5a9ebb2af5da3a3c69b56c7d1_27fd17d6;
})();

export const Button_button_06d4a8bfa391553397807c69e400e43c_27fd17d6 = /*#__PURE__*/ (() => {
const Button_button_06d4a8bfa391553397807c69e400e43c_27fd17d6 = memo(({children, ...rest}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        jsx("button",{...mergeSlotProps(rest, ({ className:"admin-search-submit", disabled:reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.users_loading_rx_state_, type:"submit" }))},children)
    )
});
Button_button_06d4a8bfa391553397807c69e400e43c_27fd17d6.displayName = "Button";
return Button_button_06d4a8bfa391553397807c69e400e43c_27fd17d6;
})();

export const Form_form_9783a3bd2a112572c7e5e7611fa29796_27fd17d6 = /*#__PURE__*/ (() => {
const Form_form_9783a3bd2a112572c7e5e7611fa29796_27fd17d6 = memo(({children, ...rest}) => {
    

    const handleSubmit_83edcced73bd4f50542adad1fce4af94 = useCallback((ev) => {
        const $form = ev.target
        ev.preventDefault()
        const form_data = {...Object.fromEntries(new FormData($form).entries()), ...({ ["admin_user_search"] : getRefValue(refs["ref_admin_user_search"]) })};

        (((...args) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___admin____admin_state.search_users", ({ ["form"] : form_data }), ({  })))], args, ({  }))))(ev));

        if (false) {
            $form.reset()
        }
    })
    


    return(
        jsx("form",{...mergeSlotProps(rest, ({ className:"admin-users-search", onSubmit:handleSubmit_83edcced73bd4f50542adad1fce4af94 }))},children)
    )
});
Form_form_9783a3bd2a112572c7e5e7611fa29796_27fd17d6.displayName = "Form";
return Form_form_9783a3bd2a112572c7e5e7611fa29796_27fd17d6;
})();

export const Bare_comp_80eb38950a2fe8f4d0eb2b48d8342d2e_27fd17d6 = /*#__PURE__*/ (() => {
const Bare_comp_80eb38950a2fe8f4d0eb2b48d8342d2e_27fd17d6 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.users_error_rx_state_
    )
});
Bare_comp_80eb38950a2fe8f4d0eb2b48d8342d2e_27fd17d6.displayName = "Bare";
return Bare_comp_80eb38950a2fe8f4d0eb2b48d8342d2e_27fd17d6;
})();

export const Cond_comp_77c3bab4ad72fd623f667af098b758df_27fd17d6 = /*#__PURE__*/ (() => {
const Cond_comp_77c3bab4ad72fd623f667af098b758df_27fd17d6 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        (!((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.users_error_rx_state_?.valueOf?.() === ""?.valueOf?.()))?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_77c3bab4ad72fd623f667af098b758df_27fd17d6.displayName = "Cond";
return Cond_comp_77c3bab4ad72fd623f667af098b758df_27fd17d6;
})();

export const Bare_comp_bb81a605686e26f7080ede907b91f2b5_27fd17d6 = /*#__PURE__*/ (() => {
const Bare_comp_bb81a605686e26f7080ede907b91f2b5_27fd17d6 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.users_notice_rx_state_
    )
});
Bare_comp_bb81a605686e26f7080ede907b91f2b5_27fd17d6.displayName = "Bare";
return Bare_comp_bb81a605686e26f7080ede907b91f2b5_27fd17d6;
})();

export const Cond_comp_d9fb49c14213a8bf2e255e8925398466_27fd17d6 = /*#__PURE__*/ (() => {
const Cond_comp_d9fb49c14213a8bf2e255e8925398466_27fd17d6 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        (!((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.users_notice_rx_state_?.valueOf?.() === ""?.valueOf?.()))?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_d9fb49c14213a8bf2e255e8925398466_27fd17d6.displayName = "Cond";
return Cond_comp_d9fb49c14213a8bf2e255e8925398466_27fd17d6;
})();

export const Cond_comp_4d7ffae3816ff1b1d6735c5d0bb5973e_27fd17d6 = /*#__PURE__*/ (() => {
const Cond_comp_4d7ffae3816ff1b1d6735c5d0bb5973e_27fd17d6 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        (reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.users_loading_rx_state_?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_4d7ffae3816ff1b1d6735c5d0bb5973e_27fd17d6.displayName = "Cond";
return Cond_comp_4d7ffae3816ff1b1d6735c5d0bb5973e_27fd17d6;
})();

export const Bare_comp_c33446d46b9e1afbabfc68ef3ab4c0b3_27fd17d6 = /*#__PURE__*/ (() => {
const Bare_comp_c33446d46b9e1afbabfc68ef3ab4c0b3_27fd17d6 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        ("Resultados: "+(JSON.stringify(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.users_total_rx_state_)))
    )
});
Bare_comp_c33446d46b9e1afbabfc68ef3ab4c0b3_27fd17d6.displayName = "Bare";
return Bare_comp_c33446d46b9e1afbabfc68ef3ab4c0b3_27fd17d6;
})();

export const Foreach_comp_de0a5f32df1d95caf68c69eeeba42cdc_27fd17d6 = /*#__PURE__*/ (() => {
const Foreach_comp_de0a5f32df1d95caf68c69eeeba42cdc_27fd17d6 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        Array.prototype.map.call(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.users_rx_state_ ?? [],((user_rx_state_,index_94e4bac005fa5971319bc02a1909793b)=>(jsx("article",{className:"admin-user-row",key:index_94e4bac005fa5971319bc02a1909793b},jsx("div",{className:"admin-user-main"},jsx("div",{},jsx("p",{className:"admin-user-name"},user_rx_state_?.["name"]),jsx("p",{className:"admin-user-username"},("@"+user_rx_state_?.["username"]))),jsx("div",{className:"admin-user-badges"},jsx("span",{className:"admin-user-id"},("ID "+user_rx_state_?.["id"])),jsx("span",{className:"admin-user-role"},user_rx_state_?.["role"]),jsx("span",{className:((user_rx_state_?.["account_status"]?.valueOf?.() === "disabled"?.valueOf?.()) ? "admin-status-disabled" : "admin-status-active")},((user_rx_state_?.["account_status"]?.valueOf?.() === "disabled"?.valueOf?.()) ? "Suspensa" : "Ativa")))),jsx("div",{className:"admin-user-controls"},jsx("div",{className:"admin-user-actions"},jsx("button",{"aria-expanded":(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.user_details_id_rx_state_?.valueOf?.() === user_rx_state_?.["id"]?.valueOf?.()),className:"quiet-button admin-user-details-toggle",onClick:((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___admin____admin_state.toggle_user_details", ({ ["user_id"] : user_rx_state_?.["id"] }), ({  })))], [_e], ({  })))),type:"button"},"Detalhes"),jsx("button",{className:((user_rx_state_?.["account_status"]?.valueOf?.() === "disabled"?.valueOf?.()) ? "quiet-button admin-user-activate" : "quiet-button admin-user-disable"),onClick:((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___admin____admin_state.open_user_status_dialog", ({ ["user_id"] : user_rx_state_?.["id"], ["status"] : ((user_rx_state_?.["account_status"]?.valueOf?.() === "disabled"?.valueOf?.()) ? "active" : "disabled") }), ({  })))], [_e], ({  })))),type:"button"},((user_rx_state_?.["account_status"]?.valueOf?.() === "disabled"?.valueOf?.()) ? "Reativar" : "Suspender"))),jsx(Fragment,{},((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.user_details_id_rx_state_?.valueOf?.() === user_rx_state_?.["id"]?.valueOf?.())?(jsx(Fragment,{},jsx("div",{className:"admin-user-details"},jsx("span",{},("Identificador: "+user_rx_state_?.["id"])),jsx("span",{},("Criada em: "+(!((user_rx_state_?.["created_at"]?.valueOf?.() === ""?.valueOf?.())) ? user_rx_state_?.["created_at"] : "N\u00e3o informado"))),jsx("span",{},("Papel: "+user_rx_state_?.["role"])),jsx("span",{},("Acesso: "+((user_rx_state_?.["account_status"]?.valueOf?.() === "disabled"?.valueOf?.()) ? "Suspenso" : "Ativo")))))):(jsx(Fragment,{},)))))))))
    )
});
Foreach_comp_de0a5f32df1d95caf68c69eeeba42cdc_27fd17d6.displayName = "Foreach";
return Foreach_comp_de0a5f32df1d95caf68c69eeeba42cdc_27fd17d6;
})();

export const Button_button_c3206e5b6cf2945cb2926bb8ca1e623c_27fd17d6 = /*#__PURE__*/ (() => {
const Button_button_c3206e5b6cf2945cb2926bb8ca1e623c_27fd17d6 = memo(({children, ...rest}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)
const on_click_a3503b478e3fca2f37d1bf2201e7ad27 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___admin____admin_state.change_users_page", ({ ["page"] : (reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.users_page_rx_state_ - 1) }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent, reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state])



    return(
        jsx("button",{...mergeSlotProps(rest, ({ className:"quiet-button", disabled:(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.users_page_rx_state_ <= 1), onClick:on_click_a3503b478e3fca2f37d1bf2201e7ad27, type:"button" }))},children)
    )
});
Button_button_c3206e5b6cf2945cb2926bb8ca1e623c_27fd17d6.displayName = "Button";
return Button_button_c3206e5b6cf2945cb2926bb8ca1e623c_27fd17d6;
})();

export const Bare_comp_d4dece1742dc939d36b9dd0cafffd26c_27fd17d6 = /*#__PURE__*/ (() => {
const Bare_comp_d4dece1742dc939d36b9dd0cafffd26c_27fd17d6 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        ("P\u00e1gina "+(JSON.stringify(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.users_page_rx_state_)))
    )
});
Bare_comp_d4dece1742dc939d36b9dd0cafffd26c_27fd17d6.displayName = "Bare";
return Bare_comp_d4dece1742dc939d36b9dd0cafffd26c_27fd17d6;
})();

export const Button_button_c05feca65e30944d8ea6af05a050cda0_27fd17d6 = /*#__PURE__*/ (() => {
const Button_button_c05feca65e30944d8ea6af05a050cda0_27fd17d6 = memo(({children, ...rest}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)
const on_click_e38962c796851825795250e945854d55 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___admin____admin_state.change_users_page", ({ ["page"] : reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.users_next_page_rx_state_ }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent, reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state])



    return(
        jsx("button",{...mergeSlotProps(rest, ({ className:"quiet-button", disabled:(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.users_next_page_rx_state_?.valueOf?.() === 0?.valueOf?.()), onClick:on_click_e38962c796851825795250e945854d55, type:"button" }))},children)
    )
});
Button_button_c05feca65e30944d8ea6af05a050cda0_27fd17d6.displayName = "Button";
return Button_button_c05feca65e30944d8ea6af05a050cda0_27fd17d6;
})();

export const Cond_comp_656bc3981ac0bd6ffc512dee98292930_27fd17d6 = /*#__PURE__*/ (() => {
const Cond_comp_656bc3981ac0bd6ffc512dee98292930_27fd17d6 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        (!((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.users_query_rx_state_?.valueOf?.() === ""?.valueOf?.()))?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_656bc3981ac0bd6ffc512dee98292930_27fd17d6.displayName = "Cond";
return Cond_comp_656bc3981ac0bd6ffc512dee98292930_27fd17d6;
})();

export const Cond_comp_088d28003d4e4fbcd484035fbb017e56_27fd17d6 = /*#__PURE__*/ (() => {
const Cond_comp_088d28003d4e4fbcd484035fbb017e56_27fd17d6 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        ((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.users_rx_state_.length > 0)?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_088d28003d4e4fbcd484035fbb017e56_27fd17d6.displayName = "Cond";
return Cond_comp_088d28003d4e4fbcd484035fbb017e56_27fd17d6;
})();

export const Bare_comp_f7b6ee18a609a209cecff3d5dea9b5c3_27fd17d6 = /*#__PURE__*/ (() => {
const Bare_comp_f7b6ee18a609a209cecff3d5dea9b5c3_27fd17d6 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        ((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.user_action_status_rx_state_?.valueOf?.() === "disabled"?.valueOf?.()) ? "Suspender conta?" : "Reativar conta?")
    )
});
Bare_comp_f7b6ee18a609a209cecff3d5dea9b5c3_27fd17d6.displayName = "Bare";
return Bare_comp_f7b6ee18a609a209cecff3d5dea9b5c3_27fd17d6;
})();

export const Bare_comp_0dd482eb0a9ecd92f66be078c9dff4d2_27fd17d6 = /*#__PURE__*/ (() => {
const Bare_comp_0dd482eb0a9ecd92f66be078c9dff4d2_27fd17d6 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        ((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.user_action_status_rx_state_?.valueOf?.() === "disabled"?.valueOf?.()) ? "A pessoa deixar\u00e1 de acessar as opera\u00e7\u00f5es protegidas at\u00e9 ser reativada." : "A pessoa poder\u00e1 voltar a acessar a conta ap\u00f3s a pr\u00f3xima autentica\u00e7\u00e3o.")
    )
});
Bare_comp_0dd482eb0a9ecd92f66be078c9dff4d2_27fd17d6.displayName = "Bare";
return Bare_comp_0dd482eb0a9ecd92f66be078c9dff4d2_27fd17d6;
})();

export const Textarea_textarea_5dbcea7b30f61f336ffdbf550c9facac_27fd17d6 = /*#__PURE__*/ (() => {
const Textarea_textarea_5dbcea7b30f61f336ffdbf550c9facac_27fd17d6 = memo(({children, ...rest}) => {
    const ref_admin_user_action_reason = useRef(null); refs["ref_admin_user_action_reason"] = ref_admin_user_action_reason;
const on_change_14c34dd561895ec606b8bfed84440fdd = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___admin____admin_state.set_user_action_reason", ({ ["value"] : _e?.["target"]?.["value"] }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])
const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        jsx("textarea",{...mergeSlotProps(rest, ({ className:"admin-user-reason", id:"admin-user-action-reason", maxLength:500, onChange:on_change_14c34dd561895ec606b8bfed84440fdd, ref:ref_admin_user_action_reason, value:reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.user_action_reason_rx_state_ }))},)
    )
});
Textarea_textarea_5dbcea7b30f61f336ffdbf550c9facac_27fd17d6.displayName = "Textarea";
return Textarea_textarea_5dbcea7b30f61f336ffdbf550c9facac_27fd17d6;
})();

export const Button_button_2f21c73006e2b2107aaeb1245df276e6_27fd17d6 = /*#__PURE__*/ (() => {
const Button_button_2f21c73006e2b2107aaeb1245df276e6_27fd17d6 = memo(({children, ...rest}) => {
    const on_click_0d26fd5ed0d84d0906480ace8a132ee9 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___admin____admin_state.close_user_status_dialog", ({  }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])
const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        jsx("button",{...mergeSlotProps(rest, ({ className:"quiet-button", disabled:reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.user_action_loading_rx_state_, onClick:on_click_0d26fd5ed0d84d0906480ace8a132ee9, type:"button" }))},children)
    )
});
Button_button_2f21c73006e2b2107aaeb1245df276e6_27fd17d6.displayName = "Button";
return Button_button_2f21c73006e2b2107aaeb1245df276e6_27fd17d6;
})();

export const Bare_comp_025348032feefe17f250c447cd6f0a2d_27fd17d6 = /*#__PURE__*/ (() => {
const Bare_comp_025348032feefe17f250c447cd6f0a2d_27fd17d6 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        (reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.user_action_loading_rx_state_ ? "Salvando\u2026" : "Confirmar")
    )
});
Bare_comp_025348032feefe17f250c447cd6f0a2d_27fd17d6.displayName = "Bare";
return Bare_comp_025348032feefe17f250c447cd6f0a2d_27fd17d6;
})();

export const Button_button_72769a8b80f54de7b8a0a7097ad59522_27fd17d6 = /*#__PURE__*/ (() => {
const Button_button_72769a8b80f54de7b8a0a7097ad59522_27fd17d6 = memo(({children, ...rest}) => {
    const on_click_1f1442115bcb17e15be27e41626a80da = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___admin____admin_state.confirm_user_status_change", ({  }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])
const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        jsx("button",{...mergeSlotProps(rest, ({ className:((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.user_action_status_rx_state_?.valueOf?.() === "disabled"?.valueOf?.()) ? "admin-dialog-confirm-danger" : "admin-dialog-confirm"), disabled:reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.user_action_loading_rx_state_, onClick:on_click_1f1442115bcb17e15be27e41626a80da, type:"button" }))},children)
    )
});
Button_button_72769a8b80f54de7b8a0a7097ad59522_27fd17d6.displayName = "Button";
return Button_button_72769a8b80f54de7b8a0a7097ad59522_27fd17d6;
})();

export const Cond_comp_6a866f4097317013c37c66396d6d65ab_27fd17d6 = /*#__PURE__*/ (() => {
const Cond_comp_6a866f4097317013c37c66396d6d65ab_27fd17d6 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        (!((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.user_action_id_rx_state_?.valueOf?.() === ""?.valueOf?.()))?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_6a866f4097317013c37c66396d6d65ab_27fd17d6.displayName = "Cond";
return Cond_comp_6a866f4097317013c37c66396d6d65ab_27fd17d6;
})();

export const Select_select_4f69d5733d4c3149c33935853a273f07_27fd17d6 = /*#__PURE__*/ (() => {
const Select_select_4f69d5733d4c3149c33935853a273f07_27fd17d6 = memo(({children, ...rest}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        jsx("select",{...mergeSlotProps(rest, ({ className:"admin-search-select", defaultValue:reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.reports_status_filter_rx_state_, name:"status" }))},children)
    )
});
Select_select_4f69d5733d4c3149c33935853a273f07_27fd17d6.displayName = "Select";
return Select_select_4f69d5733d4c3149c33935853a273f07_27fd17d6;
})();

export const Select_select_18ec46453a7a4d40824abbd0a530810a_27fd17d6 = /*#__PURE__*/ (() => {
const Select_select_18ec46453a7a4d40824abbd0a530810a_27fd17d6 = memo(({children, ...rest}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        jsx("select",{...mergeSlotProps(rest, ({ className:"admin-search-select", defaultValue:reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.reports_type_filter_rx_state_, name:"target_type" }))},children)
    )
});
Select_select_18ec46453a7a4d40824abbd0a530810a_27fd17d6.displayName = "Select";
return Select_select_18ec46453a7a4d40824abbd0a530810a_27fd17d6;
})();

export const Select_select_005dcdf1dec396f072abf6c00c430ab1_27fd17d6 = /*#__PURE__*/ (() => {
const Select_select_005dcdf1dec396f072abf6c00c430ab1_27fd17d6 = memo(({children, ...rest}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        jsx("select",{...mergeSlotProps(rest, ({ className:"admin-search-select", defaultValue:reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.reports_reason_filter_rx_state_, name:"reason" }))},children)
    )
});
Select_select_005dcdf1dec396f072abf6c00c430ab1_27fd17d6.displayName = "Select";
return Select_select_005dcdf1dec396f072abf6c00c430ab1_27fd17d6;
})();

export const Button_button_b6b07cc06cea05f6bdd0e112d3bc0e5e_27fd17d6 = /*#__PURE__*/ (() => {
const Button_button_b6b07cc06cea05f6bdd0e112d3bc0e5e_27fd17d6 = memo(({children, ...rest}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        jsx("button",{...mergeSlotProps(rest, ({ className:"admin-search-submit", disabled:reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.reports_loading_rx_state_, type:"submit" }))},children)
    )
});
Button_button_b6b07cc06cea05f6bdd0e112d3bc0e5e_27fd17d6.displayName = "Button";
return Button_button_b6b07cc06cea05f6bdd0e112d3bc0e5e_27fd17d6;
})();

export const Form_form_c584c0b580aa62186e2722135b3e9c3d_27fd17d6 = /*#__PURE__*/ (() => {
const Form_form_c584c0b580aa62186e2722135b3e9c3d_27fd17d6 = memo(({children, ...rest}) => {
    

    const handleSubmit_aaf154ea7d843ce93ba9b078cd1593f3 = useCallback((ev) => {
        const $form = ev.target
        ev.preventDefault()
        const form_data = {...Object.fromEntries(new FormData($form).entries()), ...({  })};

        (((...args) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___admin____admin_state.search_reports", ({ ["form"] : form_data }), ({  })))], args, ({  }))))(ev));

        if (false) {
            $form.reset()
        }
    })
    


    return(
        jsx("form",{...mergeSlotProps(rest, ({ className:"admin-users-search", onSubmit:handleSubmit_aaf154ea7d843ce93ba9b078cd1593f3 }))},children)
    )
});
Form_form_c584c0b580aa62186e2722135b3e9c3d_27fd17d6.displayName = "Form";
return Form_form_c584c0b580aa62186e2722135b3e9c3d_27fd17d6;
})();

export const Bare_comp_c4762a20371b77d608809c3fb1f67a40_27fd17d6 = /*#__PURE__*/ (() => {
const Bare_comp_c4762a20371b77d608809c3fb1f67a40_27fd17d6 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.reports_error_rx_state_
    )
});
Bare_comp_c4762a20371b77d608809c3fb1f67a40_27fd17d6.displayName = "Bare";
return Bare_comp_c4762a20371b77d608809c3fb1f67a40_27fd17d6;
})();

export const Cond_comp_024d6d3107412063eb615870eeb1cd19_27fd17d6 = /*#__PURE__*/ (() => {
const Cond_comp_024d6d3107412063eb615870eeb1cd19_27fd17d6 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        (!((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.reports_error_rx_state_?.valueOf?.() === ""?.valueOf?.()))?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_024d6d3107412063eb615870eeb1cd19_27fd17d6.displayName = "Cond";
return Cond_comp_024d6d3107412063eb615870eeb1cd19_27fd17d6;
})();

export const Bare_comp_0c7a34dbbc45751ec85dc7fc21e34ebd_27fd17d6 = /*#__PURE__*/ (() => {
const Bare_comp_0c7a34dbbc45751ec85dc7fc21e34ebd_27fd17d6 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.reports_notice_rx_state_
    )
});
Bare_comp_0c7a34dbbc45751ec85dc7fc21e34ebd_27fd17d6.displayName = "Bare";
return Bare_comp_0c7a34dbbc45751ec85dc7fc21e34ebd_27fd17d6;
})();

export const Cond_comp_6ce5e9703677e63e2ff341f0c04c6b31_27fd17d6 = /*#__PURE__*/ (() => {
const Cond_comp_6ce5e9703677e63e2ff341f0c04c6b31_27fd17d6 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        (!((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.reports_notice_rx_state_?.valueOf?.() === ""?.valueOf?.()))?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_6ce5e9703677e63e2ff341f0c04c6b31_27fd17d6.displayName = "Cond";
return Cond_comp_6ce5e9703677e63e2ff341f0c04c6b31_27fd17d6;
})();

export const Cond_comp_e8abac6f0fa746adae3978fa89aa17e8_27fd17d6 = /*#__PURE__*/ (() => {
const Cond_comp_e8abac6f0fa746adae3978fa89aa17e8_27fd17d6 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        (reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.reports_loading_rx_state_?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_e8abac6f0fa746adae3978fa89aa17e8_27fd17d6.displayName = "Cond";
return Cond_comp_e8abac6f0fa746adae3978fa89aa17e8_27fd17d6;
})();

export const Bare_comp_cb138a4a03a1c6abe50b70f4d506114f_27fd17d6 = /*#__PURE__*/ (() => {
const Bare_comp_cb138a4a03a1c6abe50b70f4d506114f_27fd17d6 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        ("Resultados: "+(JSON.stringify(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.reports_total_rx_state_)))
    )
});
Bare_comp_cb138a4a03a1c6abe50b70f4d506114f_27fd17d6.displayName = "Bare";
return Bare_comp_cb138a4a03a1c6abe50b70f4d506114f_27fd17d6;
})();

export const Foreach_comp_b20dabe956cf65b30952cfb367689aae_27fd17d6 = /*#__PURE__*/ (() => {
const Foreach_comp_b20dabe956cf65b30952cfb367689aae_27fd17d6 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        Array.prototype.map.call(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.reports_rx_state_ ?? [],((report_rx_state_,index_33ac9223f32a467d575207ec33092959)=>(jsx("article",{className:"admin-report-card",key:index_33ac9223f32a467d575207ec33092959},jsx("div",{className:"admin-report-heading"},jsx("div",{className:"admin-report-header-copy"},jsx("p",{className:"admin-user-name"},("Report #"+report_rx_state_?.["id"])),jsx("p",{className:"admin-user-username"},((((("Alvo: "+report_rx_state_?.["target_type"])+" #")+report_rx_state_?.["target_id"])+" \u00b7 Denunciante #")+report_rx_state_?.["reporter_user_id"]))),jsx("span",{className:"admin-user-role"},report_rx_state_?.["status"])),jsx("div",{className:"admin-report-copy"},jsx("p",{className:"admin-report-reason"},("Motivo: "+report_rx_state_?.["reason"])),jsx(Fragment,{},(!((report_rx_state_?.["description"]?.valueOf?.() === ""?.valueOf?.()))?(jsx(Fragment,{},jsx("p",{className:"admin-report-description"},report_rx_state_?.["description"]))):(jsx(Fragment,{},)))),jsx(Fragment,{},(!((report_rx_state_?.["target_snapshot"]?.valueOf?.() === ""?.valueOf?.()))?(jsx(Fragment,{},jsx("details",{className:"admin-report-context"},jsx("summary",{},"Contexto salvo no envio do report"),jsx("pre",{className:"admin-report-snapshot"},report_rx_state_?.["target_snapshot"])))):(jsx(Fragment,{},jsx("p",{className:"admin-report-description"},"Sem snapshot dispon\u00edvel."))))),jsx(Fragment,{},(!((report_rx_state_?.["decision"]?.valueOf?.() === ""?.valueOf?.()))?(jsx(Fragment,{},jsx("p",{className:"admin-report-decision"},("Decis\u00e3o registrada: "+report_rx_state_?.["decision"])))):(jsx(Fragment,{},))))),jsx("div",{className:"admin-report-actions"},jsx("button",{className:"quiet-button",disabled:reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.reports_loading_rx_state_,onClick:((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___admin____admin_state.open_report_review", ({ ["report_id"] : report_rx_state_?.["id"], ["status"] : "reviewing" }), ({  })))], [_e], ({  })))),type:"button"},"Em an\u00e1lise"),jsx("button",{className:"admin-dialog-confirm",disabled:reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.reports_loading_rx_state_,onClick:((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___admin____admin_state.open_report_review", ({ ["report_id"] : report_rx_state_?.["id"], ["status"] : "resolved" }), ({  })))], [_e], ({  })))),type:"button"},"Resolver"),jsx("button",{className:"admin-dialog-confirm-danger",disabled:reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.reports_loading_rx_state_,onClick:((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___admin____admin_state.open_report_review", ({ ["report_id"] : report_rx_state_?.["id"], ["status"] : "rejected" }), ({  })))], [_e], ({  })))),type:"button"},"Rejeitar"))))))
    )
});
Foreach_comp_b20dabe956cf65b30952cfb367689aae_27fd17d6.displayName = "Foreach";
return Foreach_comp_b20dabe956cf65b30952cfb367689aae_27fd17d6;
})();

export const Button_button_decc96c7636bdddef1c1828097c9f576_27fd17d6 = /*#__PURE__*/ (() => {
const Button_button_decc96c7636bdddef1c1828097c9f576_27fd17d6 = memo(({children, ...rest}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)
const on_click_c268673c11e9d9d3223f0998054abf15 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___admin____admin_state.change_reports_page", ({ ["page"] : (reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.reports_page_rx_state_ - 1) }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent, reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state])



    return(
        jsx("button",{...mergeSlotProps(rest, ({ className:"quiet-button", disabled:(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.reports_page_rx_state_ <= 1), onClick:on_click_c268673c11e9d9d3223f0998054abf15, type:"button" }))},children)
    )
});
Button_button_decc96c7636bdddef1c1828097c9f576_27fd17d6.displayName = "Button";
return Button_button_decc96c7636bdddef1c1828097c9f576_27fd17d6;
})();

export const Bare_comp_93c7be1954c37ca37fcaaf0045aba587_27fd17d6 = /*#__PURE__*/ (() => {
const Bare_comp_93c7be1954c37ca37fcaaf0045aba587_27fd17d6 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        ("P\u00e1gina "+(JSON.stringify(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.reports_page_rx_state_)))
    )
});
Bare_comp_93c7be1954c37ca37fcaaf0045aba587_27fd17d6.displayName = "Bare";
return Bare_comp_93c7be1954c37ca37fcaaf0045aba587_27fd17d6;
})();

export const Button_button_46ddb5c474752fc2435c27a74e7e40dd_27fd17d6 = /*#__PURE__*/ (() => {
const Button_button_46ddb5c474752fc2435c27a74e7e40dd_27fd17d6 = memo(({children, ...rest}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)
const on_click_4a1127c719a3f542185464c18efd6a62 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___admin____admin_state.change_reports_page", ({ ["page"] : reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.reports_next_page_rx_state_ }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent, reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state])



    return(
        jsx("button",{...mergeSlotProps(rest, ({ className:"quiet-button", disabled:(reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.reports_next_page_rx_state_?.valueOf?.() === 0?.valueOf?.()), onClick:on_click_4a1127c719a3f542185464c18efd6a62, type:"button" }))},children)
    )
});
Button_button_46ddb5c474752fc2435c27a74e7e40dd_27fd17d6.displayName = "Button";
return Button_button_46ddb5c474752fc2435c27a74e7e40dd_27fd17d6;
})();

export const Cond_comp_96bc27a21b9758c78ec5f8fe5b4d579b_27fd17d6 = /*#__PURE__*/ (() => {
const Cond_comp_96bc27a21b9758c78ec5f8fe5b4d579b_27fd17d6 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        ((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.reports_rx_state_.length > 0)?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_96bc27a21b9758c78ec5f8fe5b4d579b_27fd17d6.displayName = "Cond";
return Cond_comp_96bc27a21b9758c78ec5f8fe5b4d579b_27fd17d6;
})();

export const Bare_comp_5f3bf3c030acde02fe3d8628b4d12200_27fd17d6 = /*#__PURE__*/ (() => {
const Bare_comp_5f3bf3c030acde02fe3d8628b4d12200_27fd17d6 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        ((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.report_review_status_rx_state_?.valueOf?.() === "reviewing"?.valueOf?.()) ? "Iniciar an\u00e1lise?" : ((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.report_review_status_rx_state_?.valueOf?.() === "resolved"?.valueOf?.()) ? "Resolver report?" : "Rejeitar report?"))
    )
});
Bare_comp_5f3bf3c030acde02fe3d8628b4d12200_27fd17d6.displayName = "Bare";
return Bare_comp_5f3bf3c030acde02fe3d8628b4d12200_27fd17d6;
})();

export const Textarea_textarea_12760d7acc8f2307d9ad1448dcdd75ac_27fd17d6 = /*#__PURE__*/ (() => {
const Textarea_textarea_12760d7acc8f2307d9ad1448dcdd75ac_27fd17d6 = memo(({children, ...rest}) => {
    const ref_admin_report_decision = useRef(null); refs["ref_admin_report_decision"] = ref_admin_report_decision;
const on_change_5457a888ed31779bfddcd073e12dbf64 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___admin____admin_state.set_report_review_decision", ({ ["value"] : _e?.["target"]?.["value"] }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])
const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        jsx("textarea",{...mergeSlotProps(rest, ({ className:"admin-user-reason", id:"admin-report-decision", maxLength:2000, onChange:on_change_5457a888ed31779bfddcd073e12dbf64, ref:ref_admin_report_decision, value:reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.report_review_decision_rx_state_ }))},)
    )
});
Textarea_textarea_12760d7acc8f2307d9ad1448dcdd75ac_27fd17d6.displayName = "Textarea";
return Textarea_textarea_12760d7acc8f2307d9ad1448dcdd75ac_27fd17d6;
})();

export const Button_button_ba42b10efd0b6780c809739b035f4558_27fd17d6 = /*#__PURE__*/ (() => {
const Button_button_ba42b10efd0b6780c809739b035f4558_27fd17d6 = memo(({children, ...rest}) => {
    const on_click_5c673a2c321234f0fba756ce519a67ef = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___admin____admin_state.close_report_review", ({  }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])
const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        jsx("button",{...mergeSlotProps(rest, ({ className:"quiet-button", disabled:reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.report_review_loading_rx_state_, onClick:on_click_5c673a2c321234f0fba756ce519a67ef, type:"button" }))},children)
    )
});
Button_button_ba42b10efd0b6780c809739b035f4558_27fd17d6.displayName = "Button";
return Button_button_ba42b10efd0b6780c809739b035f4558_27fd17d6;
})();

export const Bare_comp_56181417cbb93c69beafd6f498656087_27fd17d6 = /*#__PURE__*/ (() => {
const Bare_comp_56181417cbb93c69beafd6f498656087_27fd17d6 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        (reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.report_review_loading_rx_state_ ? "Salvando\u2026" : "Confirmar decis\u00e3o")
    )
});
Bare_comp_56181417cbb93c69beafd6f498656087_27fd17d6.displayName = "Bare";
return Bare_comp_56181417cbb93c69beafd6f498656087_27fd17d6;
})();

export const Button_button_bdfc3e7b9c98eb0beb19d3bab6c8a506_27fd17d6 = /*#__PURE__*/ (() => {
const Button_button_bdfc3e7b9c98eb0beb19d3bab6c8a506_27fd17d6 = memo(({children, ...rest}) => {
    const on_click_ea3cc53ce1e7a0717e1276db0982d3b9 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.codeboxd_main___state___session____session_state.codeboxd_main___state___admin____admin_state.save_report_review", ({  }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])
const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        jsx("button",{...mergeSlotProps(rest, ({ className:"admin-dialog-confirm", disabled:reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.report_review_loading_rx_state_, onClick:on_click_ea3cc53ce1e7a0717e1276db0982d3b9, type:"button" }))},children)
    )
});
Button_button_bdfc3e7b9c98eb0beb19d3bab6c8a506_27fd17d6.displayName = "Button";
return Button_button_bdfc3e7b9c98eb0beb19d3bab6c8a506_27fd17d6;
})();

export const Cond_comp_138b362fa718a3f95c396b7cc4ce6a30_27fd17d6 = /*#__PURE__*/ (() => {
const Cond_comp_138b362fa718a3f95c396b7cc4ce6a30_27fd17d6 = memo(({children}) => {
    const reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state = useContext(StateContexts.reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state)



    return(
        (!((reflex___state____state__codeboxd_main___state___session____session_state__codeboxd_main___state___admin____admin_state.report_review_id_rx_state_?.valueOf?.() === ""?.valueOf?.()))?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_138b362fa718a3f95c396b7cc4ce6a30_27fd17d6.displayName = "Cond";
return Cond_comp_138b362fa718a3f95c396b7cc4ce6a30_27fd17d6;
})();
