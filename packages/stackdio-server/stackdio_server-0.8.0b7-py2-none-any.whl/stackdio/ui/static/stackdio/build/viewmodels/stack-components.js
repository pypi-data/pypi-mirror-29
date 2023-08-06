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

define(["jquery","knockout","models/stack"],function(e,n,t){"use strict";return function(){var o=this;o.stack=null,o.breadcrumbs=[{active:!1,title:"Stacks",href:"/stacks/"},{active:!1,title:window.stackdio.stackTitle,href:"/stacks/"+window.stackdio.stackId+"/"},{active:!0,title:"Components"}],o.availableComponents=n.observableArray(),o.selectedComponent=n.observable(),o.hostTarget=n.observable(),o.reset=function(){o.stack=new t(window.stackdio.stackId,o),o.availableComponents([]),o.selectedComponent(null),o.hostTarget(null)},o.openMap={},o.refreshComponents=function(){o.stack.loadComponents().done(function(){0==o.availableComponents().length&&o.availableComponents(o.stack.components()),Object.keys(o.openMap).forEach(function(n){o.openMap[n]&&e("#"+n).addClass("in")}),o.stack.components().forEach(function(n){var t=e("#"+n.htmlId);t.on("show.bs.collapse",function(){o.openMap[n.htmlId]=!0}),t.on("hide.bs.collapse",function(){o.openMap[n.htmlId]=!1})}),o.openId})},o.reload=function(){o.refreshComponents(),o.selectedComponent(null),o.hostTarget(null)},o.runSingle=function(){o.stack.runSingleSls(o.selectedComponent().sls_path,o.hostTarget()).done(function(){})},o.reset(),o.refreshComponents(),setInterval(o.refreshComponents,3e3)}});