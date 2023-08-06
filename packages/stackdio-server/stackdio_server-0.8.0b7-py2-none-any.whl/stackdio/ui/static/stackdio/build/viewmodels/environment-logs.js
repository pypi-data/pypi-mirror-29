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

define(["jquery","knockout","bootbox","utils/utils","models/environment","fuelux"],function(e,t,o,n,l){"use strict";return function(){var o=this;o.breadcrumbs=[{active:!1,title:"Environments",href:"/environments/"},{active:!1,title:window.stackdio.environmentName,href:"/environments/"+window.stackdio.environmentName+"/"},{active:!0,title:"Logs"}],o.selectedLogUrl=null,o.log=t.observable(),o.environment=t.observable(),o.reset=function(){o.environment(new l(window.stackdio.environmentName,o)),o.selectedLogUrl=null,o.log("Select a log...")},o.reload=function(t){void 0===t&&(t=!1),o.selectedLogUrl&&(t&&o.log("Loading..."),e.ajax({method:"GET",url:o.selectedLogUrl,headers:{Accept:"text/plain"}}).done(function(e){var n=document.getElementById("log-text"),l=n.scrollTop,r=n.scrollHeight;o.log(e),(r-l<550||t)&&(n.scrollTop=n.scrollHeight-498)}).fail(function(e){403==e.status?window.location.reload(!0):n.growlAlert("Failed to load log","danger")}))},o.dataSource=function(e,t){var n;"Latest"===e.text?n=o.environment().latestLogs():"Historical"===e.text?n=o.environment().historicalLogs():(o.environment().loadLogs(),n=[{text:"Latest",type:"folder"},{text:"Historical",type:"folder"}]),t({data:n})},o.reset();var r=e("#log-selector");r.tree({dataSource:o.dataSource,cacheItems:!1,folderSelect:!1}),o.intervalId=null,r.on("selected.fu.tree",function(e,t){o.selectedLogUrl=t.target.url,clearInterval(o.intervalId),o.reload(!0),t.target.url.indexOf("latest")>=0&&(o.intervalId=setInterval(o.reload,3e3))})}});