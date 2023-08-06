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

define(["jquery","knockout","bootbox","utils/utils","models/user"],function(e,o,r,n,t){"use strict";return function(){var s=this;s.user=null,s.userTokenShown=o.observable(),s.userToken=o.observable(),s.apiRootUrl=o.observable(),s.breadcrumbs=[{active:!0,title:"User Profile"}],s.subscription=null,s.reset=function(){s.subscription&&s.subscription.dispose(),s.user=new t(null,s),s.userTokenShown(!1),s.userToken(null),s.apiRootUrl(window.location.origin+"/api/");var o=e(".checkbox-custom");s.subscription=s.user.advanced.subscribe(function(e){e?o.checkbox("check"):o.checkbox("uncheck")}),s.user.waiting.done(function(){s.user.loadGroups()})},s.promptPassword=function(e,o){r.prompt({title:e,inputType:"password",callback:function(e){e&&o(e)}})},s.showUserToken=function(){s.promptPassword("Enter password to retrieve token",function(o){e.ajax({method:"POST",url:"/api/user/token/",data:JSON.stringify({username:s.user.username(),password:o})}).done(function(e){s.userToken(e.token),s.userTokenShown(!0)}).fail(function(e){n.growlAlert("Failed to retrieve API token.  Make sure you entered the correct password.","danger")})})},s.resetUserToken=function(){s.promptPassword("Enter password to reset token",function(o){r.confirm({title:"Confirm token reset",message:"Are you sure you want to reset your API token?  It will permanently be deleted and will be deactivated immediately.",callback:function(r){r&&e.ajax({method:"POST",url:"/api/user/token/reset/",data:JSON.stringify({username:s.user.username(),password:o})}).done(function(e){s.userToken(e.token),s.userTokenShown(!0)}).fail(function(e){n.growlAlert("Failed to reset API token.  Make sure you entered the correct password.","danger")})}})})},s.reset()}});