import { Component }       from "@angular/core";
import { BrowseService }   from "./browse.service";
import { SettingsService } from "./settings.service";
import { GuessItService }  from "./guessit.service";

@Component({
    selector: 'hl-browse',
    template: `
    <form>
        <div class="container-fluid">
            <div class="pull-left">
                <div class="checkbox">
                    <label><input name="showWithoutLinksOnlyCheckbox" type="checkbox" [(ngModel)]="showWithoutLinksOnly">Show without links only</label>
                </div>
            </div>
        </div>
        <hl-links-table [withoutLinksOnly]="showWithoutLinksOnly"></hl-links-table>
    </form>
    `,
    providers: [ BrowseService, SettingsService, GuessItService ]
})
export class BrowseComponent {
    showWithoutLinksOnly = true;

    constructor() {
    }
}
