import { Component }     from "@angular/core";

@Component({
    template: `
    <form>
        <div class="container-fluid">
            <div class="pull-left">
                <div class="checkbox">
                    <label><input name="showWithoutLinksOnlyCheckbox" type="checkbox" [ngModel]="showWithoutLinksOnly" (ngModelChanged)="showWithoutLinksOnly = $event">Show without links only</label>
                </div>
            </div>
            <div class="pull-right">
                <div class="checkbox">
                    <label><input name="showAbsolutePathCheckbox" type="checkbox"  [ngModel]="showAbsolutePath" (ngModelChanged)="showAbsolutePath = $event">Show absolute path</label>
                </div>
            </div>
        </div>
        <hl-links-table></hl-links-table>
    </form>
    `,
})
export class BrowseComponent {
    showWithoutLinksOnly = true;
    showAbsolutePath = false;

    constructor() {
    }
}
