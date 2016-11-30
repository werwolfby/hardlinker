import { Component, OnInit, Input }          from '@angular/core';
import { FileInfo, LinkInfo, BrowseService } from "./browse.service";
import { BehaviorSubject }                   from "rxjs/BehaviorSubject";
import "rxjs/add/operator/combineLatest";

@Component({
    selector: 'hl-links-table',
    template: `
    <table class="table table-striped">
        <tr>
            <th width="50%">Source</th>
            <th width="50%">Dest</th>
        </tr>
        <tr *ngFor="let file of files">
            <td width="50%"><file-info [file]="file"></file-info></td>
            <td width="50%" *ngIf="file.links && file.links.length > 0"><file-info *ngFor="let link of file.links" [file]="link"></file-info></td>
            <td width="50%" *ngIf="!file.links || file.links.length == 0"><guess-it [file]="file"></guess-it></td>
        </tr>
    </table>
    `
})
export class LinksTableComponent implements OnInit {
    private _withoutLinksOnlyObservable: BehaviorSubject<boolean> = new BehaviorSubject(false);

    public files : LinkInfo[] = [];

    @Input()
    public set withoutLinksOnly(value: boolean) {
        this._withoutLinksOnlyObservable.next(value);
    }

    constructor(private _browseService : BrowseService) {
    }

    ngOnInit() {
        var allFiles = this._browseService.getAll();

        var files = allFiles
            .combineLatest(this._withoutLinksOnlyObservable, 
                           (files, withoutLinksOnly) => files.filter(r => !withoutLinksOnly || ((r.links ? r.links.length : 0) == 0)))
            .subscribe(files => this.files = files);
    }
}