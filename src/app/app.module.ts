import { NgModule }              from '@angular/core';
import { FormsModule }           from '@angular/forms';
import { BrowserModule }         from '@angular/platform-browser';
import { RouterModule }          from '@angular/router';
import { HttpModule }            from '@angular/http';
import { AppComponent }          from "./app.component"
import { AppRoutingModule }      from "./app-routing.module"
import { BrowseComponent }       from "./browse/browse.component"
import { FileInfoComponent }     from "./browse/file-info.component"
import { LinksTableComponent }   from "./browse/links-table.component";
import { GuessItComponent }      from "./browse/guessit.component";

import './../app.css';

@NgModule({
    imports: [
        BrowserModule,
        AppRoutingModule,
        FormsModule,
        HttpModule,
    ],
    declarations: [
        AppComponent,
        BrowseComponent,
        FileInfoComponent,
        LinksTableComponent,
        GuessItComponent
    ],
    bootstrap: [ AppComponent ],
})
export class AppModule { }