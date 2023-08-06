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

define(["jquery","knockout","bootbox","models/environment"],function(e,r,n,t){"use strict";return function(){var e=this;e.environment=new t(window.stackdio.environmentName),e.breadcrumbs=[{active:!1,title:"Environments",href:"/environments/"},{active:!1,title:window.stackdio.environmentName,href:"/environments/"+window.stackdio.environmentName+"/"},{active:!0,title:"Properties"}],e.validProperties=!0,e.propertiesJSON=r.pureComputed({read:function(){return r.toJSON(e.environment.properties(),null,3)},write:function(r){try{e.environment.properties(JSON.parse(r)),e.validProperties=!0}catch(r){e.validProperties=!1}}}),e.saveProperties=function(){if(!e.validProperties)return void n.alert({title:"Error saving properties",message:"The properties field must contain valid JSON."});e.environment.saveProperties()},e.reload=function(){e.environment.loadProperties()},e.reload()}});