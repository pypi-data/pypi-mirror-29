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

define([],function(){var t=!1,n=/xyz/.test(function(){xyz})?/\b_super\b/:/.*/,e=function(){};return e.extend=function(e){function i(){!t&&this.init&&this.init.apply(this,arguments)}var r=this.prototype;t=!0;var o=new this;t=!1;for(var u in e)o[u]="function"==typeof e[u]&&"function"==typeof r[u]&&n.test(e[u])?function(t,n){return function(){var e=this._super;this._super=r[t];var i=n.apply(this,arguments);return this._super=e,i}}(u,e[u]):e[u];return i.prototype=o,i.prototype.constructor=i,i.extend=arguments.callee,i},e});