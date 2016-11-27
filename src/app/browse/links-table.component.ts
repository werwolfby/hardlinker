import { Component, OnInit }                 from '@angular/core';
import { FileInfo, LinkInfo, BrowseService } from "./browse.service";


@Component({
    selector: 'hl-links-table',
    template: `
    <table class="table table-striped">
        <tr>
            <th width="50%">Source</th>
            <th width="50%">Dest</th>
        </tr>
        <tr *ngFor="let file of files">
            <td width="50%">{{file.name}}</td>
            <td width="50%">{{file.links}}</td>
        </tr>
    </table>
    `,
    providers: [ BrowseService ]
})
export class LinksTableComponent implements OnInit {
    public files : LinkInfo[] = [];

    constructor(private _browseService : BrowseService) {
    }

    ngOnInit() {
        this._browseService
            .getAll()
            .subscribe(files => {
                this.files = files
            });
    }
}