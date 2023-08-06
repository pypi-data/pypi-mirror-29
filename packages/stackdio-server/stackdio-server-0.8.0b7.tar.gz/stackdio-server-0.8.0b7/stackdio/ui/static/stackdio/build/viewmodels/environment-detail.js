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

define(["jquery","knockout","models/environment","fuelux"],function(n,e,i){"use strict";return function(){var o=this;o.environment=null,o.environmentUrl=e.observable(""),o.breadcrumbs=[{active:!1,title:"Environments",href:"/environments/"},{active:!0,title:window.stackdio.environmentName}],o.subscription=null,o.reset=function(){o.subscription&&o.subscription.dispose(),o.environment=new i(window.stackdio.environmentName,o),o.environment.waiting.done(function(){document.title="stackd.io | Environment Detail - "+o.environment.name()}).fail(function(){window.location="/environments/"});var e=n(".checkbox-custom");o.subscription=o.environment.createUsers.subscribe(function(n){n?e.checkbox("check"):e.checkbox("uncheck")})},o.refreshEnvironment=function(){o.environment.refreshActivity().fail(function(){window.location="/environments/"})},n(".action-dropdown").on("show.bs.dropdown",function(){o.environment.loadAvailableActions()}),o.reset(),o.refreshEnvironment(),setInterval(o.refreshEnvironment,3e3)}});