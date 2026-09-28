import {Link as ReactRouterLink} from "react-router"
import LucideShieldCheck from "lucide-react/dist/esm/icons/shield-check.mjs"
import {Fragment,useEffect,useRef} from "react"
import {refs} from "$/utils/state"
import {Bare_comp_8d0d0dbe9e52451ab479605fae6a66af_27fd17d6,Bare_comp_bd554523900b9b74daaac23eac57e50a_27fd17d6,Button_button_a65a61e4175cca1466521caec7ff335a_27fd17d6,Button_button_d65dd17558c5527c576be3b0fe1c1843_27fd17d6,Cond_comp_d2b0fe9982d8d79ffc1f395127db034c_27fd17d6,Dynamicicon_dynamicicon_ac530eeee0a26e6f0f2e534b611544cf_27fd17d6,Form_form_471d8f94ea188278ade7d000a265231b_27fd17d6,Input_input_531865e9a11759a5188ffabe009a6422_27fd17d6} from "$/app_components/Codeboxd_main/pages/admin"
import {jsx} from "@emotion/react"





function Component() {
const ref_admin_email = useRef(null); refs["ref_admin_email"] = ref_admin_email;




  return (
    jsx(Fragment,{},jsx("main",{className:"admin-login-page"},jsx("section",{className:"admin-login-layout"},jsx(ReactRouterLink,{"aria-label":"Codeboxd \u2014 in\u00edcio",className:"brand admin-login-brand",to:"/"},jsx("svg",{className:"w-10 h-10 text-[#F5B300] flex-shrink-0",css:({ ["fill"] : "none", ["stroke"] : "currentColor", ["strokeLinecap"] : "round", ["strokeLinejoin"] : "round", ["strokeWidth"] : "2.5" }),viewBox:"0 0 44 44"},jsx("path",{css:({ ["stroke"] : "#F5B300", ["strokeWidth"] : "2.6" }),d:"M22 3L40 13.5V34.5L22 45L4 34.5V13.5L22 3Z"},),jsx("path",{css:({ ["stroke"] : "#F5B300", ["strokeWidth"] : "2.6" }),d:"M22 3V24M4 13.5L22 24M40 13.5L22 24"},),jsx("path",{css:({ ["stroke"] : "#F5B300", ["strokeWidth"] : "1.8" }),d:"M9 22.5L12 25L9 27.5"},),jsx("path",{css:({ ["fill"] : "#F5B300", ["stroke"] : "#F5B300", ["strokeWidth"] : "1.2" }),d:"M31 22.5L35 25L31 27.5V22.5Z"},)),jsx("span",{},"code",jsx("span",{className:"brand-yellow"},"boxd"))),jsx("div",{className:"admin-login-card"},jsx("div",{"aria-hidden":"true",className:"admin-login-icon"},jsx(LucideShieldCheck,{size:22},)),jsx("p",{className:"admin-login-eyebrow"},"\u00c1REA RESTRITA"),jsx("h1",{className:"admin-login-title"},"Acesso administrativo"),jsx("p",{className:"admin-login-description"},"Entre com uma conta autorizada para gerenciar o Codeboxd."),jsx(Form_form_471d8f94ea188278ade7d000a265231b_27fd17d6,{},jsx("div",{},jsx("label",{className:"admin-login-label",htmlFor:"admin_email"},"E-mail"),jsx("input",{autoComplete:"username",className:"admin-login-input",id:"admin_email",name:"email",placeholder:"voce@exemplo.com",ref:ref_admin_email,required:true,type:"email"},)),jsx("div",{},jsx("label",{className:"admin-login-label",htmlFor:"admin_password"},"Senha"),jsx("div",{className:"admin-password-field"},jsx(Input_input_531865e9a11759a5188ffabe009a6422_27fd17d6,{},),jsx(Button_button_d65dd17558c5527c576be3b0fe1c1843_27fd17d6,{},jsx(Dynamicicon_dynamicicon_ac530eeee0a26e6f0f2e534b611544cf_27fd17d6,{},)))),jsx("div",{className:"admin-login-options"},jsx("label",{className:"admin-remember-label"},jsx("input",{defaultChecked:true,name:"remember",type:"checkbox"},)," Manter sess\u00e3o neste dispositivo"),jsx(ReactRouterLink,{className:"admin-login-link",to:"/redefinir-senha"},"Esqueci minha senha")),jsx(Fragment,{},jsx(Cond_comp_d2b0fe9982d8d79ffc1f395127db034c_27fd17d6,{},jsx(Fragment,{},jsx("p",{className:"admin-login-error",role:"alert"},jsx(Bare_comp_bd554523900b9b74daaac23eac57e50a_27fd17d6,{},))),jsx(Fragment,{},))),jsx(Button_button_a65a61e4175cca1466521caec7ff335a_27fd17d6,{},jsx(Bare_comp_8d0d0dbe9e52451ab479605fae6a66af_27fd17d6,{},)))),jsx(ReactRouterLink,{className:"admin-login-back",to:"/login"},"Voltar ao login do Codeboxd"))),jsx("title",{},"Acesso administrativo | Codeboxd"),jsx("meta",{content:"favicon.ico",property:"og:image"},))
  )
}
Component.displayName = "Component(admin/login)";

export default Component;
