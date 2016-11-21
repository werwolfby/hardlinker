import { Component } from "@angular/core";
//import {LinksTableComponent} from "./links-table.component";

@Component({
    template: `
    <form>
        <div class="container-fluid">
            <div class="pull-left">
                <div class="checkbox">
                    <label><input type="checkbox">Show without links only</label>
                </div>
            </div>
            <div class="pull-right">
                <div class="checkbox">
                    <label><input type="checkbox">Show absolute path</label>
                </div>
            </div>
        </div>
    </form>
    `,
    //directives: [LinksTableComponent]
})
export class BrowseComponent {
    showWithoutLinksOnly = true;
    showAbsolutePath = false;

    constructor() {
    }
}
