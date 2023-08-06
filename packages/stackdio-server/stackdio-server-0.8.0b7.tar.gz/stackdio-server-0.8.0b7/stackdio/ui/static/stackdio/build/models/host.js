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

define(["jquery","underscore","knockout","bootbox"],function(e,t,s,a){"use strict";function i(e,t){var a=!1;"string"==typeof e&&(e=parseInt(e)),"number"==typeof e&&(a=!0,e={id:e,url:"/api/stacks/"+e+"/hosts/"}),this.raw=e,this.parent=t,this.id=e.id,this.hostname=s.observable(),this.fqdn=s.observable(),this.publicDNS=s.observable(),this.privateDNS=s.observable(),this.hostDefinition=s.observable(),this.activity=s.observable(),this.health=s.observable(),this.labelClass=s.observable(),this.healthLabelClass=s.observable(),a?this.reload():this._process(e)}return i.constructor=i,i.prototype._process=function(e){switch(this.hostname(e.hostname),this.fqdn(e.fqdn),this.publicDNS(e.provider_public_dns),this.privateDNS(e.provider_private_dns),this.hostDefinition(e.blueprint_host_definition),this.activity(e.activity),this.health(e.health),e.activity){case"idle":this.labelClass("label-success");break;case"launching":case"provisioning":case"orchestrating":case"resuming":case"pausing":case"executing":case"terminating":this.labelClass("label-warning");break;case"queued":case"paused":case"terminated":this.labelClass("label-info");break;case"dead":this.labelClass("label-danger");break;case"unknown":default:this.labelClass("label-default")}switch(e.health){case"healthy":this.healthLabelClass("label-success");break;case"unstable":this.healthLabelClass("label-warning");break;case"unhealthy":this.healthLabelClass("label-danger");break;case"unknown":default:this.healthLabelClass("label-default")}},i.prototype.reload=function(){var t=this;return e.ajax({method:"GET",url:this.raw.url}).done(function(e){t.raw=e,t._process(e)})},i.prototype.delete=function(){var t=this;a.confirm({title:"Confirm delete of <strong>"+stackTitle+"</strong>",message:"Are you sure you want to delete <strong>"+stackTitle+"</strong>?<br>This will terminate all infrastructure, in addition to removing all history related to this stack.",buttons:{confirm:{label:"Delete",className:"btn-danger"}},callback:function(s){s&&e.ajax({method:"DELETE",url:t.raw.url}).done(function(e){t.raw=e,t._process(e)}).fail(function(e){var t;try{var s=JSON.parse(e.responseText);t=s.detail.join("<br>")}catch(e){t="Oops... there was a server error.  This has been reported to your administrators."}a.alert({title:"Error deleting stack",message:t})})}})},i});