import { NgModule }              from '@angular/core';
import { FormsModule }           from '@angular/forms';
import { BrowserModule }         from '@angular/platform-browser';
import { RouterModule }          from '@angular/router';
import { AppComponent }          from "./app.component"
import { AppRoutingModule }      from "./app-routing.module"
import { BrowseComponent }       from "./browse/browse.component"
import { LinksTableComponent }   from "./browse/links-table.component";

import './../app.css';

@NgModule({
    imports: [ 
        BrowserModule,
        AppRoutingModule,
        FormsModule,
    ],
    declarations: [ AppComponent, BrowseComponent, LinksTableComponent ],
    bootstrap:    [ AppComponent ],
})
export class AppModule { }