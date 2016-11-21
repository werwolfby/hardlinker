import { NgModule }            from '@angular/core';
import { BrowserModule }       from '@angular/platform-browser';
import { RouterModule }        from '@angular/router';
import { AppComponent }        from "./app.component"
import { AppRoutingModule }    from "./app-routing.module"
import { BrowseComponent }     from "./browse/browse.component"

import './../app.css';

@NgModule({
    imports: [ 
        BrowserModule,
        AppRoutingModule
    ],
    declarations: [ AppComponent, BrowseComponent ],
    bootstrap:    [ AppComponent ],
})
export class AppModule { }