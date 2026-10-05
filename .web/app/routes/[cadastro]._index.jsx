import {Link as ReactRouterLink} from "react-router"
import {Fragment,useEffect,useRef} from "react"
import {refs} from "$/utils/state"
import {Bare_comp_74c3925696748caf399eacc402ccec7d_24663de3,Bare_comp_d6ddc95630766b330eb2ccc495464542_24663de3,Button_button_6121de223ccfd37a1dd51ccba7e9901a_24663de3,Cond_comp_d0da96d081f6234401b69e992074904a_24663de3,Form_form_0d63a0582c47089970dce39beb90a70c_24663de3} from "$/app_components/Codeboxd_main/pages/account"
import {jsx} from "@emotion/react"





function Component() {
const ref_name = useRef(null); refs["ref_name"] = ref_name;
const ref_username = useRef(null); refs["ref_username"] = ref_username;
const ref_email = useRef(null); refs["ref_email"] = ref_email;
const ref_password = useRef(null); refs["ref_password"] = ref_password;
const ref_confirm_password = useRef(null); refs["ref_confirm_password"] = ref_confirm_password;




  return (
    jsx(Fragment,{},jsx("main",{className:"min-h-screen bg-black text-white flex justify-center items-center p-8"},jsx("div",{className:"signup-layout"},jsx("section",{className:"signup-intro"},jsx(ReactRouterLink,{className:"brand",to:"/"},jsx("svg",{className:"w-10 h-10 text-[#F5B300] flex-shrink-0",css:({ ["fill"] : "none", ["stroke"] : "currentColor", ["strokeLinecap"] : "round", ["strokeLinejoin"] : "round", ["strokeWidth"] : "2.5" }),viewBox:"0 0 44 44"},jsx("path",{css:({ ["stroke"] : "#F5B300", ["strokeWidth"] : "2.6" }),d:"M22 3L40 13.5V34.5L22 45L4 34.5V13.5L22 3Z"},),jsx("path",{css:({ ["stroke"] : "#F5B300", ["strokeWidth"] : "2.6" }),d:"M22 3V24M4 13.5L22 24M40 13.5L22 24"},),jsx("path",{css:({ ["stroke"] : "#F5B300", ["strokeWidth"] : "1.8" }),d:"M9 22.5L12 25L9 27.5"},),jsx("path",{css:({ ["fill"] : "#F5B300", ["stroke"] : "#F5B300", ["strokeWidth"] : "1.2" }),d:"M31 22.5L35 25L31 27.5V22.5Z"},)),jsx("span",{},"code",jsx("span",{className:"brand-yellow"},"boxd"))),jsx("h1",{className:"text-4xl font-bold leading-tight"},"Suas hist\u00f3rias merecem companhia."),jsx("p",{className:"text-gray-400 leading-relaxed"},"Salve o que voc\u00ea quer assistir ou ler, avalie suas descobertas e encontre sua comunidade."),jsx("img",{alt:"Mascote Codeboxd",src:"/mascot.png"},)),jsx("section",{className:"signup-panel"},jsx("h2",{className:"text-2xl font-bold mb-2"},"Fa\u00e7a parte da comunidade"),jsx("p",{className:"text-gray-400 mb-8 text-sm"},"Crie sua conta e comece sua cole\u00e7\u00e3o."),jsx(Form_form_0d63a0582c47089970dce39beb90a70c_24663de3,{},jsx("div",{},jsx("label",{className:"block text-sm text-gray-300 mb-2",htmlFor:"name"},"Seu nome"),jsx("input",{autoComplete:"name",className:"form-input-custom w-full h-12 px-4 rounded-xl text-white",id:"name",maxLength:80,name:"name",ref:ref_name,required:true,type:"text"},)),jsx("div",{},jsx("label",{className:"block text-sm text-gray-300 mb-2",htmlFor:"username"},"Nome de usu\u00e1rio"),jsx("input",{autoComplete:"username",className:"form-input-custom w-full h-12 px-4 rounded-xl text-white",id:"username",maxLength:30,minLength:3,name:"username",pattern:"[a-zA-Z0-9_]{3,30}",ref:ref_username,required:true,title:"Use de 3 a 30 letras, n\u00fameros ou sublinhados.",type:"text"},)),jsx("div",{},jsx("label",{className:"block text-sm text-gray-300 mb-2",htmlFor:"email"},"E-mail"),jsx("input",{autoComplete:"email",className:"form-input-custom w-full h-12 px-4 rounded-xl text-white",id:"email",name:"email",ref:ref_email,required:true,type:"email"},)),jsx("div",{},jsx("label",{className:"block text-sm text-gray-300 mb-2",htmlFor:"password"},"Senha"),jsx("input",{autoComplete:"new-password",className:"form-input-custom w-full h-12 px-4 rounded-xl text-white",id:"password",minLength:8,name:"password",ref:ref_password,required:true,type:"password"},)),jsx("p",{className:"text-xs text-gray-400"},"Use pelo menos 8 caracteres, incluindo letra e n\u00famero."),jsx("div",{},jsx("label",{className:"block text-sm text-gray-300 mb-2",htmlFor:"confirm_password"},"Confirme a senha"),jsx("input",{autoComplete:"new-password",className:"form-input-custom w-full h-12 px-4 rounded-xl text-white",id:"confirm_password",minLength:8,name:"confirm_password",ref:ref_confirm_password,required:true,type:"password"},)),jsx("label",{className:"text-sm"},jsx("input",{name:"remember",type:"checkbox"},)," Manter-me conectado"),jsx(Fragment,{},jsx(Cond_comp_d0da96d081f6234401b69e992074904a_24663de3,{},jsx(Fragment,{},jsx("p",{className:"text-red-400",role:"alert"},jsx(Bare_comp_d6ddc95630766b330eb2ccc495464542_24663de3,{},))),jsx(Fragment,{},))),jsx(Button_button_6121de223ccfd37a1dd51ccba7e9901a_24663de3,{},jsx(Bare_comp_74c3925696748caf399eacc402ccec7d_24663de3,{},))),jsx(ReactRouterLink,{className:"block mt-6 text-[#F5B300]",to:"/login"},"J\u00e1 tenho conta")))),jsx("title",{},"CodeboxdMain | Cadastro"),jsx("meta",{content:"favicon.ico",property:"og:image"},))
  )
}
Component.displayName = "Component(cadastro)";

export default Component;
