/*!
  * Copyright 2017,  Digital Reasoning
  *
  * Licensed under the Apache License, Version 2.0 (the "License");
  * you may not use this file except in compliance with the License.
  * You may obtain a copy of the License at
  *
  *     http://www.apache.org/licenses/LICENSE-2.0
  *
  * Unless required by applicable law or agreed to in writing, software
  * distributed under the License is distributed on an "AS IS" BASIS,
  * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  * See the License for the specific language governing permissions and
  * limitations under the License.
  *
*/

define(["jquery","knockout","ladda","bootbox","utils/utils","select2"],function(e,r,t,a,o){"use strict";return function(){var o=this;o.breadcrumbs=[{active:!1,title:"Formulas",href:"/formulas/"},{active:!0,title:"Import"}],o.uriSelector=e("#formulaUri"),o.uriSelector.select2({data:[],theme:"bootstrap",placeholder:"Select a formula...",disabled:!0}),o.uriSelector.on("select2:select",function(e){var r=e.params.data;o.uri(r.clone_url)}),o.uri=r.observable(),o.sshPrivateKey=r.observable(),o.subscription=null,o.loadRepos=function(){e.ajax({method:"GET",url:"https://api.github.com/orgs/stackdio-formulas/repos"}).done(function(e){e.forEach(function(e){e.text=e.name}),o.uriSelector.select2({data:e.sort(function(e,r){return e.name<r.name?-1:e.name>r.name?1:0}),theme:"bootstrap",placeholder:"Select a formula...",disabled:!1,minimumInputLength:0,templateResult:function(e){return e.loading?e.text:e.description?e.name+" ("+e.description+")":e.name}})}).fail(function(){console.warn("Could not load default list of formulas: Github API rate limit exceeded");var r=e(".select2-container");r.attr({"data-toggle":"tooltip","data-placement":"top",title:"Could not load default list of formulas: Github API rate limit exceeded"}),r.tooltip()})},o.reset=function(){o.uri(""),o.sshPrivateKey("")},o.removeErrors=function(r){r.forEach(function(r){var t=e("#"+r);t.removeClass("has-error"),t.find(".help-block").remove()})},o.importFormula=function(){var r=["uri","ssh_private_key"];o.removeErrors(r);var i=t.create(document.querySelector("#import-button"));i.start(),e.ajax({method:"POST",url:"/api/formulas/",data:JSON.stringify({uri:o.uri(),ssh_private_key:o.sshPrivateKey()})}).always(function(){i.stop()}).done(function(){window.location="/formulas/"}).fail(function(t){var o="";try{var i=JSON.parse(t.responseText);for(var s in i)if(i.hasOwnProperty(s))if(r.indexOf(s)>=0){var l=e("#"+s);l.addClass("has-error"),i[s].forEach(function(e){l.append('<span class="help-block">'+e+"</span>")})}else if("non_field_errors"===s)i[s].forEach(function(r){if(r.indexOf("uri")>=0){var t=e("#uri");t.addClass("has-error"),t.append('<span class="help-block">A formula with this URI already exists.</span>')}});else{var n=s.replace("_"," ");i[s].forEach(function(e){o+="<dt>"+n+"</dt><dd>"+e+"</dd>"})}o&&(o='<dl class="dl-horizontal">'+o+"</dl>")}catch(e){o="Oops... there was a server error.  This has been reported to your administrators."}o&&a.alert({title:"Error importing formula",message:o})})},o.reset(),o.loadRepos()}});