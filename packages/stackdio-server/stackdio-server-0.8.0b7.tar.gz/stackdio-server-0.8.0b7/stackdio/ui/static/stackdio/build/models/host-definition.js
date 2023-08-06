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

define(["jquery","knockout","utils/utils","models/formula-component","models/access-rule","models/blueprint-volume"],function(e,t,s,o,i,r){"use strict";function n(e,s){this.raw=e,this.id=e.id,this.parent=s,this.title=t.observable(),this.description=t.observable(),this.cloudImage=t.observable(),this.count=t.observable(),this.hostnameTemplate=t.observable(),this.size=t.observable(),this.isSpot=t.observable(),this.spotPrice=t.observable(),this.zone=t.observable(),this.subnetId=t.observable(),this.components=t.observableArray([]),this.accessRules=t.observableArray([]),this.volumes=t.observableArray([]),this._process(e)}return n.constructor=n,n.prototype._process=function(e){this.title(e.title),this.description(e.description),this.cloudImage(e.cloud_image),this.count(e.count),this.hostnameTemplate(e.hostname_template),this.size(e.size),this.zone(e.zone),this.subnetId(e.subnet_id),this.spotPrice(e.spot_price),this.isSpot(!!this.spotPrice());var t=this;this.components(e.formula_components.map(function(e){return new o(e,t.parent,t)})),this.accessRules(e.access_rules.map(function(e){return new i(e,t.parent,t)})),this.volumes(e.volumes.map(function(e){return new r(e,t.parent,t)}))},n.prototype.save=function(){var t=this,o=["title","description","hostname_template","subnet_id","zone","spot_price"];return o.forEach(function(t){var s=e("#"+t);s.removeClass("has-error"),s.find(".help-block").remove()}),e.ajax({method:"PUT",url:t.raw.url,data:JSON.stringify({title:t.title(),description:t.description(),hostname_template:t.hostnameTemplate(),subnet_id:t.subnetId(),zone:t.zone(),spot_price:t.isSpot()?t.spotPrice():null})}).done(function(e){s.growlAlert("Successfully saved host definition.","success")}).fail(function(e){s.parseSaveError(e,"blueprint",o)})},n});