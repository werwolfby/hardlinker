import { Component, OnInit, Input }           from '@angular/core';
import { FileInfo, LinkInfo, FileInfoObject } from "./file-info";
import { BrowseService }                      from "./browse.service";
import { GuessItService }                     from "./guessit.service";
import { BehaviorSubject }                    from "rxjs/BehaviorSubject";
import "rxjs/add/operator/combineLatest";

@Component({
    selector: 'hl-links-table',
    template: `
    <table class="table table-striped">
        <tr>
            <th width="50%">Source</th>
            <th width="50%">
                <span>Dest </span>
                <a (click)="guessall()" class="btn btn-primary btn-xs"><span class="glyphicon glyphicon-link" aria-hidden="true"></span><span>Guess All</span></a>
                <a (click)="linkall()" class="btn btn-success btn-xs" [class.disabled]="!hasGuess"><span class="glyphicon glyphicon-link" aria-hidden="true"></span><span>Link All</span></a>
            </th>
        </tr>
        <tr *ngFor="let file of files">
            <td width="50%"><file-info [file]="file"></file-info></td>
            <td width="50%" *ngIf="file.hasLinks"><file-info *ngFor="let link of file.links" [file]="link"></file-info></td>
            <td width="50%" *ngIf="!file.hasLinks"><guess-it [file]="file"></guess-it></td>
        </tr>
    </table>
    `
})
export class LinksTableComponent implements OnInit {
    private _withoutLinksOnlyObservable: BehaviorSubject<boolean> = new BehaviorSubject(false);
    files : FileInfoObject[] = [];

    @Input()
    public set withoutLinksOnly(value: boolean) {
        this._withoutLinksOnlyObservable.next(value);
    }

    get hasGuess() : boolean {
        for (let file of this.files) {
            if (file.guess) {
                return true;
            }
        }

        return false;
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

    private _findFile(fileInfo : FileInfo) : FileInfoObject {
        let files = this.files.filter(f => f.equals(fileInfo));
        return files.length > 0 ? files[0] : null;
    }

    ngOnInit() {
        var allFiles = this._browseService.getAll();

        allFiles
            .combineLatest(this._withoutLinksOnlyObservable,
                           (files, withoutLinksOnly) => files.filter(r => !withoutLinksOnly || !r.hasLinks))
            .subscribe(files => this.files = files);
    }
}