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

define(["jquery","knockout","models/blueprint","models/host-definition","fuelux"],function(i,t,n,e){"use strict";return function(){var o=this;o.blueprint=new n(window.stackdio.blueprintId),o.currentHostDefinition=t.observable(null),o.hostDefinitionModal=i("#edit-host-definition-modal"),o.subsciption=null,o.breadcrumbs=[{active:!1,title:"Blueprints",href:"/blueprints/"},{active:!1,title:window.stackdio.blueprintTitle,href:"/blueprints/"+window.stackdio.blueprintId+"/"},{active:!0,title:"Host Definitions"}],o.reload=function(){o.blueprint.waiting.done(function(){o.blueprint.loadHostDefinitions()})},o.editHostDefinition=function(t){o.currentHostDefinition(new e(t.raw)),o.hostDefinitionModal.modal("show");var n=i(".checkbox-custom");o.currentHostDefinition().isSpot()?n.checkbox("check"):n.checkbox("uncheck")},o.saveHostDefinition=function(){o.currentHostDefinition().save().done(function(i){o.hostDefinitionModal.modal("hide"),o.currentHostDefinition(null),o.blueprint.loadHostDefinitions()})},o.reload()}});