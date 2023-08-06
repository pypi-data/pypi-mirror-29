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

define(["jquery","generics/pagination","models/formula"],function(t,i,a){"use strict";return i.extend({breadcrumbs:[{active:!0,title:"Formulas"}],model:a,baseUrl:"/formulas/",initialUrl:"/api/formulas/",sortableFields:[{name:"title",displayName:"Title",width:"25%"},{name:"uri",displayName:"Repo URL",width:"55%"},{name:"status",displayName:"Status",width:"10%"}],openActionFormulaId:null,actionMap:{},reset:function(){this.openActionFormulaId=null,this.actionMap={},this._super()},processObject:function(t){this.actionMap.hasOwnProperty(t.id)&&t.availableActions(this.actionMap[t.id])},extraReloadSteps:function(){var i=t(".action-dropdown"),a=this;i.on("show.bs.dropdown",function(t){var i=parseInt(t.target.id);a.openActionFormulaId=i;for(var o=a.objects(),n=0,e=o.length;n<e;++n)if(o[n].id===i){o[n].loadAvailableActions();break}}),i.on("hide.bs.dropdown",function(){a.openActionFormulaId=null})}})});