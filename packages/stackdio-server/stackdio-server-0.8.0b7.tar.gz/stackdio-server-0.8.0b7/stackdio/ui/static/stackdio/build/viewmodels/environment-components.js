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

define(["jquery","knockout","models/environment"],function(n,e,o){"use strict";return function(){var t=this;t.environment=null,t.breadcrumbs=[{active:!1,title:"Environments",href:"/environments/"},{active:!1,title:window.stackdio.environmentName,href:"/environments/"+window.stackdio.environmentName+"/"},{active:!0,title:"Components"}],t.availableComponents=e.observableArray(),t.selectedComponent=e.observable(),t.hostTarget=e.observable(),t.reset=function(){t.environment=new o(window.stackdio.environmentName,t),t.availableComponents([]),t.selectedComponent(null),t.hostTarget(null)},t.openMap={},t.refreshComponents=function(){t.environment.loadComponents().done(function(){0==t.availableComponents().length&&t.availableComponents(t.environment.components()),Object.keys(t.openMap).forEach(function(e){t.openMap[e]&&n("#"+e).addClass("in")}),t.environment.components().forEach(function(e){var o=n("#"+e.htmlId);o.on("show.bs.collapse",function(){t.openMap[e.htmlId]=!0}),o.on("hide.bs.collapse",function(){t.openMap[e.htmlId]=!1})}),t.openId})},t.reload=function(){t.refreshComponents(),t.selectedComponent(null),t.hostTarget(null)},t.runSingle=function(){t.environment.runSingleSls(t.selectedComponent().sls_path,t.hostTarget()).done(function(){})},t.reset(),t.refreshComponents(),setInterval(t.refreshComponents,3e3)}});