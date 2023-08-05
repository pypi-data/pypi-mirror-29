BOWERDEPS="undefined"==typeof BOWERDEPS?{}:BOWERDEPS,function(){var t,e;t=function(){function t(){return["ui.router","ui.bootstrap","ngAnimate","guanlecoja.ui","bbData"]}return t}(),e=function(){function t(t,e,s){e.addGroup({name:"grid",caption:"Grid View",icon:"cubes",order:4}),t.state({name:"grid",controller:"gridController",controllerAs:"C",templateUrl:"grid_view/views/grid.html",url:"/grid?branch&tag&result",reloadOnSearch:!1,data:{group:"grid",caption:"Grid View"}}),s.addSettingsGroup({name:"Grid",caption:"Grid related settings",items:[{type:"bool",name:"fullChanges",caption:"Show avatar and time ago in change details",defaultValue:!1},{type:"bool",name:"leftToRight",caption:"Show most recent changes on the right",defaultValue:!1},{type:"integer",name:"revisionLimit",caption:"Maximum number of revisions to display",default_value:5},{type:"integer",name:"changeFetchLimit",caption:"Maximum number of changes to fetch",default_value:100},{type:"integer",name:"buildFetchLimit",caption:"Maximum number of builds to fetch",default_value:1e3}]})}return t}(),angular.module("grid_view",new t).config(["$stateProvider","glMenuServiceProvider","bbSettingsServiceProvider",e])}.call(this),function(){var t,e=function(t,e){return function(){return t.apply(e,arguments)}},s={}.hasOwnProperty;t=function(){function t(t,s,i,a,n,r){var l,h,u,g;this.$scope=t,this.$stateParams=s,this.$state=i,this.isTagToggled=e(this.isTagToggled,this),this.isBuilderDisplayed=e(this.isBuilderDisplayed,this),this.refresh=e(this.refresh,this),this.resetTags=e(this.resetTags,this),this.toggleTag=e(this.toggleTag,this),this.changeResult=e(this.changeResult,this),this.changeBranch=e(this.changeBranch,this),this.onChange=e(this.onChange,this),_.mixin(this.$scope,a),this.data=n.open().closeOnDestroy(this.$scope),this.branch=this.$stateParams.branch,this.tags=null!=(h=this.$stateParams.tag)?h:[],angular.isArray(this.tags)||(this.tags=[this.tags]),this.result=this.$stateParams.result,this.results=function(){var t,e;t=a.resultsTexts,e=[];for(l in t)g=t[l],e.push({code:l+"",text:g});return e}(),u=r.getSettingsGroup("Grid"),this.revisionLimit=u.revisionLimit.value,this.changeFetchLimit=u.changeFetchLimit.value,this.buildFetchLimit=u.buildFetchLimit.value,this.fullChanges=u.fullChanges.value,this.leftToRight=u.leftToRight.value,this.buildsets=this.data.getBuildsets({limit:this.buildFetchLimit,order:"-bsid"}),this.changes=this.data.getChanges({limit:this.changeFetchLimit,order:"-changeid"}),this.builders=this.data.getBuilders(),this.buildrequests=this.data.getBuildrequests({limit:this.buildFetchLimit,order:"-buildrequestid"}),this.builds=this.data.getBuilds({limit:this.buildFetchLimit,order:"-buildrequestid"}),this.buildsets.onChange=this.changes.onChange=this.builders.onChange=this.buildrequests.change=this.builds.onChange=this.onChange}return t.prototype.dataReady=function(){var t,e,s,i;for(i=[this.buildsets,this.changes,this.builders,this.buildrequests,this.builds],e=0,s=i.length;s>e;e++)if(t=i[e],!(t.$resolved&&t.length>0))return!1;return!0},t.prototype.dataFetched=function(){var t,e,s,i;for(i=[this.buildsets,this.changes,this.builders,this.buildrequests,this.builds],e=0,s=i.length;s>e;e++)if(t=i[e],!t.$resolved)return!1;return!0},t.prototype.onChange=function(){var t,e,i,a,n,r,l,h,u,g,o,c,d,b,p,f,m,v,C,y,$,T,w,B,P,L,R,S,F,x,q,D,G,O,k,E,V,M,A,N,W,I;if(this.dataReady()){for(c={},e={},d={},D=this.changes,f=0,C=D.length;C>f;f++)g=D[f],d[g.sourcestamp.ssid]=g,g.buildsets={};for(G=this.buildsets,m=0,y=G.length;y>m;m++)i=G[m],o=d[_.last(i.sourcestamps).ssid],null!=o&&(o.buildsets[i.bsid]=i,null==o.branch&&(o.branch="master"),e[o.branch]=!0,this.branch&&o.branch!==this.branch||(c[o.changeid]=o));for(c=function(){var t;t=[];for(b in c)s.call(c,b)&&(o=c[b],t.push(o));return t}(),this.leftToRight?(c.sort(function(t,e){return t.changeid-e.changeid}),c.length>this.revisionLimit&&(c=c.slice(c.length-this.revisionLimit))):(c.sort(function(t,e){return e.changeid-t.changeid}),c.length>this.revisionLimit&&(c=c.slice(0,this.revisionLimit))),this.$scope.changes=c,this.$scope.branches=function(){var s;s=[];for(t in e)s.push(t);return s}(),I={},O=this.buildrequests,v=0,$=O.length;$>v;v++)N=O[v],(null!=I[S=N.buildsetid]?I[S]:I[S]=[]).push(N);for(u={},k=this.builds,L=0,T=k.length;T>L;L++)n=k[L],(null!=u[F=n.buildrequestid]?u[F]:u[F]=[]).push(n);for(E=this.builders,R=0,w=E.length;w>R;R++)r=E[R],r.builds={};for(l={},V=this.$scope.changes,x=0,B=V.length;B>x;x++){g=V[x],M=g.buildsets;for(a in M)if(s.call(M,a)&&(i=M[a],W=I[a],null!=W))for(q=0,P=W.length;P>q;q++){if(N=W[q],h=null!=(A=u[N.buildrequestid])?A:[],null!=this.result&&""!==this.result&&!isNaN(this.result))for(p=0;p<h.length;)parseInt(h[p].results)!==parseInt(this.result)?h.splice(p,1):p+=1;h.length>0&&(r=this.builders.get(h[0].builderid),this.isBuilderDisplayed(r)&&(l[r.builderid]=r,r.builds[g.changeid]=h))}}return this.$scope.builders=function(){var t;t=[];for(p in l)s.call(l,p)&&(r=l[p],t.push(r));return t}()}},t.prototype.changeBranch=function(t){return this.branch=t,this.refresh()},t.prototype.changeResult=function(t){return this.result=t,this.refresh()},t.prototype.toggleTag=function(t){var e;return e=this.tags.indexOf(t),0>e?this.tags.push(t):this.tags.splice(e,1),this.refresh()},t.prototype.resetTags=function(){return this.tags=[],this.refresh()},t.prototype.refresh=function(){var t;return this.$stateParams.branch=this.branch,0===this.tags.length?this.$stateParams.tag=void 0:this.$stateParams.tag=this.tags,this.$stateParams.result=this.result,t={branch:this.$stateParams.branch,tag:this.$stateParams.tag,result:this.$stateParams.result},this.$state.transitionTo(this.$state.current,t,{notify:!1}),this.onChange()},t.prototype.isBuilderDisplayed=function(t){var e,s,i,a;for(i=this.tags,e=0,s=i.length;s>e;e++)if(a=i[e],t.tags.indexOf(a)<0)return!1;return!0},t.prototype.isTagToggled=function(t){return this.tags.indexOf(t)>=0},t}(),angular.module("grid_view").controller("gridController",["$scope","$stateParams","$state","resultsService","dataService","bbSettingsService",t])}.call(this),angular.module("grid_view").run(["$templateCache",function(t){t.put("grid_view/views/grid.html",'<div class="container grid"><div class="load-indicator" ng-hide="C.dataFetched()"><div class="spinner"><i class="fa fa-circle-o-notch fa-spin fa-2x"></i><p>loading</p></div></div><p ng-show="C.dataFetched() &amp;&amp; C.changes.length == 0">No changes. Grid View needs a changesource to be setup, and<a href="#/changes"> changes</a> to be in the system.</p><div class="form-inline" ng-show="C.dataReady()"><div class="form-group"><label>Branch</label><select class="form-control" ng-model="C.branch" ng-change="C.changeBranch(C.branch)" ng-options="br for br in branches | orderBy"><option value="">(all)</option></select></div><div class="form-group"><label>Results</label><select class="form-control" ng-model="C.result" ng-change="C.changeResult(C.result)" ng-options="r.code as r.text for r in C.results"><option value="">(all)</option></select></div></div><table class="table table-condensed table-striped table-hover" ng-show="C.dataReady()"><thead><tr><th>Builder</th><th><span ng-show="C.tags.length == 0">Tags</span><span ng-show="C.tags.length &lt; 5" ng-repeat="tag in C.tags"><span class="builder-tag label clickable label-success" ng-click="C.toggleTag(tag)">{{ tag }}</span></span><span ng-show="C.tags.length &gt;= 5"><span class="label label-success">{{ C.tags.length }} tags</span></span><span ng-show="C.tags.length &gt; 0"><span class="label label-danger clickable" ng-click="C.resetTags()" uib-tooltip="Reset tags filter">x</span></span></th><th class="change" ng-repeat="ch in changes track by ch.changeid"><changedetails change="ch" compact="!C.fullChanges"></changedetails></th></tr></thead><tbody><tr ng-repeat="b in builders | orderBy: \'name\'"><th><a ui-sref="builder({builder: b.builderid})">{{ b.name }}</a></th><td><span ng-repeat="tag in b.tags"><span class="builder-tag label clickable" ng-click="C.toggleTag(tag)" ng-class="C.isTagToggled(tag) ? \'label-success\': \'label-default\'">{{ tag }}</span></span></td><td ng-repeat="ch in changes track by ch.changeid"><a ng-repeat="build in b.builds[ch.changeid] | orderBy: \'buildid\'" ui-sref="build({builder: b.builderid, build: build.number})"><span class="badge-status" ng-class="results2class(build, \'pulse\')">{{ build.number }}</span></a></td></tr></tbody></table></div>')}]);