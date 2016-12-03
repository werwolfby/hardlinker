import { Component, OnInit, Input }          from '@angular/core';
import { FileInfo, LinkInfo, BrowseService } from "./browse.service";
import { GuessItService }                    from "./guessit.service";
import { BehaviorSubject }                   from "rxjs/BehaviorSubject";
import "rxjs/add/operator/combineLatest";

interface GuessInfo extends LinkInfo {
    guess: FileInfo    
}

@Component({
    selector: 'hl-links-table',
    template: `
    <table class="table table-striped">
        <tr>
            <th width="50%">Source</th>
            <th width="50%">Dest <a (click)="guessall()" class="btn btn-primary btn-xs"><span class="glyphicon glyphicon-link" aria-hidden="true"></span><span> Guess All</span></a></th>
        </tr>
        <tr *ngFor="let file of files">
            <td width="50%"><file-info [file]="file"></file-info></td>
            <td width="50%" *ngIf="file.links && file.links.length > 0"><file-info *ngFor="let link of file.links" [file]="link"></file-info></td>
            <td width="50%" *ngIf="!file.links || file.links.length == 0"><guess-it [file]="file" [newLink]="file.guess"></guess-it></td>
        </tr>
    </table>
    `
})
export class LinksTableComponent implements OnInit {
    private _withoutLinksOnlyObservable: BehaviorSubject<boolean> = new BehaviorSubject(false);

    public files : GuessInfo[] = [];

    @Input()
    public set withoutLinksOnly(value: boolean) {
        this._withoutLinksOnlyObservable.next(value);
    }

    constructor(private _browseService : BrowseService, private _guessItService : GuessItService) {
    }

    public guessall() {
        this._guessItService.guessall()
            .subscribe(links => this._updateFiles(links));
    }

    private _updateFiles(links : LinkInfo[]) {
        for (let link of links) {
            let file = this._findFile(link);
            if (file == null) {
                continue;                
            }

            file.guess = link.links[0];
        }
    }

    private _findFile(fileInfo : FileInfo) : GuessInfo {
        let files = this.files.filter(f => f.folder == fileInfo.folder && this._isEqualArray(f.path, fileInfo.path) && f.name == fileInfo.name)
        return files.length > 0 ? files[0] : null;
    }

    private _isEqualArray(a1, a2) {
        if (a1 == null && a2 == null) {
            return true;
        }

        if (a1 == null || a2 == null) {
            return false;
        }

        return a1.length == a2.length && a1.every(function(v,i) { return v === a2[i]});
    }

    ngOnInit() {
        var allFiles = this._browseService.getAll();

        var files = allFiles
            .combineLatest(this._withoutLinksOnlyObservable, 
                           (files, withoutLinksOnly) => files.filter(r => !withoutLinksOnly || ((r.links ? r.links.length : 0) == 0)))
            .subscribe(files => this.files = files.map(f => <GuessInfo> Object.assign({}, f)));
    }
}