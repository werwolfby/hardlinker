import { Component }       from "@angular/core";
import { BrowseComponent } from "./browse/browse.component"

@Component({
    selector: 'hl-app',
    template: `
    <nav class="navbar navbar-inverse navbar-fixed-top">
        <div class="container-fluid">
            <div class="navbar-header">
                <a class="navbar-brand" href="/">Hard Linker</a>
            </div>
        </div>
    </nav>

    <div class="container-fluid">

        <div class="hard-linker">
            <hl-browse></hl-browse>
        </div>

    </div>    
    `,
})
export class AppComponent {
}
