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

define(["jquery","generics/pagination","models/environment"],function(n,i,e){"use strict";return i.extend({breadcrumbs:[{active:!0,title:"Environments"}],model:e,baseUrl:"/environments/",initialUrl:"/api/environments/",detailRequiresAdvanced:!0,sortableFields:[{name:"name",displayName:"Name",width:"20%"},{name:"description",displayName:"Description",width:"35%"},{name:"labelList",displayName:"Labels",width:"15%"},{name:"activity",displayName:"Activity",width:"10%"},{name:"health",displayName:"Health",width:"10%"}],openActionEnvironmentId:null,actionMap:{},reset:function(){this.openActionEnvironmentId=null,this.actionMap={},this._super()},processObject:function(n){this.actionMap.hasOwnProperty(n.id)&&n.availableActions(this.actionMap[n.id])},extraReloadSteps:function(){var i=n(".action-dropdown"),e=this;i.on("show.bs.dropdown",function(n){var i=n.target.id;e.openActionEnvironmentId=i;for(var t=e.objects(),a=0,o=t.length;a<o;++a)if(t[a].id===i){t[a].loadAvailableActions();break}}),i.on("hide.bs.dropdown",function(){e.openActionEnvironmentId=null})}})});