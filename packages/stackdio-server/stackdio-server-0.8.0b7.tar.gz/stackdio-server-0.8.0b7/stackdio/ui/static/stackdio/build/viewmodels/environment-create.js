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

define(["jquery","knockout","ladda","bootbox","utils/formula-versions","models/formula-version","fuelux","select2"],function(e,r,o,n,s,a){"use strict";return function(){var a=this;a.breadcrumbs=[{active:!1,title:"Environments",href:"/environments/"},{active:!0,title:"New"}],a.name=r.observable(),a.description=r.observable(),a.properties=r.observable({}),a.formulaVersions=r.observableArray([]),a.formulas=null,a.versionsReady=r.observable(),a.validProperties=!0,a.createButton=null,a.propertiesJSON=r.pureComputed({read:function(){return r.toJSON(a.properties(),null,3)},write:function(e){try{a.properties(JSON.parse(e)),a.validProperties=!0}catch(e){a.validProperties=!1}}}),a.subscription=null,a.reset=function(){a.name(""),a.description(""),a.properties({}),a.formulaVersions([]),a.versionsReady(!1)},a.createSelectors=function(){var e=[];a.formulaVersions().forEach(function(r){s.createVersionSelector(r,a.formulas)||e.push(r)}),e.forEach(function(e){a.formulaVersions.remove(e)}),a.versionsReady(!0)},a.removeErrors=function(r){r.forEach(function(r){var o=e("#"+r);o.removeClass("has-error"),o.find(".help-block").remove()})},a.getVersionsData=function(){return a.formulaVersions().map(function(e){return{formula:e.formula(),version:e.version()}})},a.createEnvironment=function(){var r=["name","description","properties"];if(a.removeErrors(r),!a.validProperties){var s=e("#properties");return s.addClass("has-error"),void s.append('<span class="help-block">Invalid JSON.</span>')}var t=o.create(document.querySelector("#create-button"));t.start(),e.ajax({method:"POST",url:"/api/environments/",data:JSON.stringify({name:a.name(),description:a.description(),properties:a.properties(),formula_versions:a.getVersionsData()})}).always(function(){t.stop()}).done(function(){window.location="/environments/"}).fail(function(o){var s="";try{var a=JSON.parse(o.responseText);for(var t in a)if(a.hasOwnProperty(t))if(r.indexOf(t)>=0){var i=e("#"+t);i.addClass("has-error"),a[t].forEach(function(e){i.append('<span class="help-block">'+e+"</span>")})}else if("non_field_errors"===t)a[t].forEach(function(r){if(r.indexOf("name")>=0){var o=e("#name");o.addClass("has-error"),o.append('<span class="help-block">A environment with this name already exists.</span>')}});else{var l=t.replace("_"," ");a[t].forEach(function(e){s+="<dt>"+l+"</dt><dd>"+e+"</dd>"})}s&&(s='<dl class="dl-horizontal">'+s+"</dl>")}catch(e){s="Oops... there was a server error.  This has been reported to your administrators."}s&&n.alert({title:"Error creating environment",message:s})})},a.reset()}});