/* ---- shared additions (both themes): toggle, maps, rich-text tables. No layout changes to template blocks. ---- */
.theme-toggle{display:inline-flex;align-items:center;justify-content:center;width:38px;height:38px;min-width:38px;padding:0;margin-right:10px;border-radius:50%;border:1px solid currentColor;background:transparent;color:#fff;cursor:pointer;opacity:.85;transition:opacity .2s}
.theme-toggle:hover,.theme-toggle:focus-visible{opacity:1}
.theme-toggle svg{width:18px;height:18px;display:block}
.theme-toggle .ico-sun{display:none}
.navbar.v2 .theme-toggle{color:#000}
.nav-menu-button-wrapper{display:flex;align-items:center}
.svw-map{border-radius:12px;overflow:hidden;line-height:0}
.svw-map iframe{width:100%;height:260px;border:0;display:block}
.footer .svw-map{margin-top:24px}
.footer .svw-map iframe{height:200px}
.svw-nap a,.svw-links a{text-decoration:underline;text-underline-offset:3px}
.svw-links{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:32px;margin-top:40px}
.svw-links ul{margin:12px 0 0;padding-left:20px}
.svw-links li{margin-bottom:8px}
.svw-group-title{margin:56px 0 8px}
.svw-group-title:first-child{margin-top:0}
.detail-text table{width:100%;border-collapse:collapse;margin:16px 0 24px;font-size:15px}
.detail-text th,.detail-text td{border:1px solid #0000001f;padding:10px 12px;text-align:left;vertical-align:top}
.detail-text th{background:#f3f1eb}
.detail-text blockquote{border-left:3px solid #c1f85f;margin:16px 0;padding:4px 0 4px 16px}
.detail-text a{text-decoration:underline;text-underline-offset:3px}
.svw-sources li{font-size:14px;line-height:1.45}
.service-details-wrapper .detail-text h2{margin-top:40px;margin-bottom:16px}
.service-details-wrapper .detail-text h2:first-child{margin-top:0}
.service-details-wrapper .detail-text h3{margin-top:28px}
.service-details-wrapper .detail-text p{margin-bottom:14px}
.service-details-wrapper .detail-text ul,.service-details-wrapper .detail-text ol{margin-bottom:18px}
.button-wrap.svw-two{display:inline-flex;flex-wrap:wrap;gap:10px}
@media (max-width:479px){.theme-toggle{width:34px;height:34px;min-width:34px;margin-right:6px}}

/* ---- dark theme. %D% is expanded twice: once for the OS preference, once for the stored toggle. ---- */
%D% body{
  --_color-pallet---white-shade--bg-color:#10120e;
  --_color-pallet---white-shade--card-bg:#1b1e18;
  --_color-pallet---dark-shade--black:#efede6;
  --_color-pallet---dark-shade--body-text-dark:#bdbcb3;
  --_color-pallet---dark-shade--stroke:#8d8c84;
  --_color-pallet---border-color--border-100:#ffffff21;
  background-color:#10120e;color:#efede6}
%D% .theme-toggle .ico-sun{display:block}
%D% .theme-toggle .ico-moon{display:none}
%D% .navbar.v2 .theme-toggle{color:#efede6}
/* keep dark text on the lime buttons and the white arrow circles */
%D% .button,%D% .button .button-text,%D% .submit-button{color:#000}
%D% .submit-button:hover{background-color:#efede6;color:#000}
%D% .utility-page-wrap.v2{background-color:#000}
%D% .error-message{background-color:#2a1414;color:#fff}
/* dark logos and dark line icons sitting on now-dark surfaces */
%D% .navbar.v2 .brand-logo,%D% .navbar.v2 .brand-logo-text,%D% .logo,%D% .choose-icon,%D% .benefit-iteam .icon,
%D% .health-info-title .icon,%D% .contact-info-wrap .icon,%D% .explore-icon,%D% .social-icon{filter:invert(1) brightness(1.1)}
%D% .text-field,%D% .w-select{background-color:#14170f;color:#efede6}
%D% .text-field::placeholder{color:#8d8c84}
%D% .w-tab-link,%D% .w-tab-link .text-h4{color:#efede6}
%D% .drop-inner-box{background-color:#14170f}
%D% .blog-category,%D% .history-category{background-color:#efede6}
%D% .detail-text th{background:#1b1e18}
%D% .detail-text th,%D% .detail-text td{border-color:#ffffff24}
%D% .svw-map iframe{filter:invert(.9) hue-rotate(180deg) brightness(.95)}
%D% .w-form-done{color:#000}
%D% img.footer-shape{opacity:.12}
