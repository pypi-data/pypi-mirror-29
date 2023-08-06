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

define(["jquery","knockout","bootbox","generics/pagination","models/stack","models/volume"],function(e,t,a,i,s,d){"use strict";return i.extend({breadcrumbs:[{active:!1,title:"Stacks",href:"/stacks/"},{active:!1,title:window.stackdio.stackTitle,href:"/stacks/"+window.stackdio.stackId+"/"},{active:!0,title:"Volumes"}],autoRefresh:!1,model:d,baseUrl:"/stacks/",initialUrl:"/api/stacks/"+window.stackdio.stackId+"/volumes/",sortableFields:[{name:"volumeId",displayName:"Volume ID",width:"15%"},{name:"snapshotId",displayName:"Snapshot",width:"20%"},{name:"size",displayName:"Size",width:"15%"},{name:"device",displayName:"Device",width:"15%"},{name:"mountPoint",displayName:"Mount Point",width:"20%"},{name:"encrypted",displayName:"Encrypted",width:"15%"}]})});