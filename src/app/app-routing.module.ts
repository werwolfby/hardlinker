import { NgModule }             from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { BrowseComponent }      from "./browse/browse.component"

const routes: Routes = [
    { path: '', redirectTo: '/browse', pathMatch: 'full' },
    { path: 'browse',  component: BrowseComponent },
];

@NgModule({
    imports: [ RouterModule.forRoot(routes) ],
    exports: [ RouterModule ]
})
export class AppRoutingModule {}
