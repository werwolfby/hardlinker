import { Component, OnInit, Input }              from '@angular/core';
import { FileInfo, LinkInfo, BrowseService }     from "./browse.service";
import { SettingsService, Settings, FolderInfo } from "./settings.service";
import { Observable, BehaviorSubject }           from "rxjs";
import "rxjs/add/operator/combineLatest";

@Component({
    selector: 'guess-it',
    template: `<div [ngSwitch]="state">
        <template [ngSwitchCase]="0"><a (click)="guessit()" class="btn btn-primary btn-xs"><span class="glyphicon glyphicon-link" aria-hidden="true"></span><span> Guess It</span></a></template>
        <template [ngSwitchCase]="1">...loading...</template>
        <template [ngSwitchCase]="2">
            <div *ngIf="!editLink">
                <button (click)="startEdit()" class="btn btn-primary btn-xs" type="submit">
                    <span class="glyphicon glyphicon-pencil" aria-hidden="true"></span>
                    <span> Edit</span>
                </button>
                <button (click)="cancel()" class="btn btn-warning btn-xs" type="submit">
                    <span class="glyphicon glyphicon-remove" aria-hidden="true"></span>
                    <span> Cancel</span>
                </button>
                <file-info [file]="newLink"></file-info>
                <button (click)="link()"  class="btn btn-success btn-xs" type="submit">
                    <span class="glyphicon glyphicon-link"   aria-hidden="true"></span>
                    <span> Link</span>
                </button>
            </div>
            <div *ngIf="editLink">
                <div class="form-inline">
                    <div class="form-group">
                        <button (click)="cancelEdit()" class="btn btn-primary btn-xs" type="submit">
                            <span class="glyphicon glyphicon-remove" aria-hidden="true"></span>
                            <span>Cancel</span>
                        </button>
                    </div>
                    <div class="form-group">
                        <div class="input-group input-group-sm">
                            <div class="input-group-btn">
                                <button type="button" class="btn btn-default dropdown-toggle" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false"><span class="caret"></span> {{getFolderPathByName(editLink.folder)}}{{editSettings.pathSeparator}}</button>
                                <ul class="dropdown-menu">
                                    <li *ngFor="let f of rootFolders" [class.active]="editLink.folder == f.name"><a (click)="setRootFolder(f.name)">{{getFolderPath(f)}}{{editSettings.pathSeparator}}</a></li>
                                </ul>
                            </div>
                            <input type="text" class="form-control" [ngModel]="getPath(editLink)" (blur)="setPath(editLink, $event.target.value)" placeholder="folder">
                            <div class="input-group-addon">{{editSettings.pathSeparator}}</div>
                            <input type="text" class="form-control" [(ngModel)]="editLink.name" placeholder="name">
                        </div>
                    </div>
                    <div class="form-group">
                        <button (click)="saveEdit()" class="btn btn-primary btn-xs" type="submit">
                            <span class="glyphicon glyphicon-ok" aria-hidden="true"></span>
                            <span>Save</span>
                        </button>
                    </div>
                </div>
            </div>
        </template>
        <template [ngSwitchCase]="3">...linking...</template>
    </div>`,
})
export class GuessItComponent implements OnInit {
    private state: number = 0;
    private newLink: FileInfo;
    private editLink: FileInfo;
    private rootFolders: FolderInfo[] = [];
    private editSettings: Settings;
    private _settings: Observable<Settings>;
    private _outputFolders: Observable<FolderInfo[]>;
    @Input()
    public absolutePath : boolean;

    constructor(private _settingsService: SettingsService) {
    }

    private guessit() {
        this.state = 1;
        setTimeout(this.onGuess({folder: "Shows", path: ["Show1", "Season 1"], name: "file.mp4"}), 0.7);
    }

    private onGuess(data: FileInfo) {
        this.state = 2;
        this.newLink = data;
    }
    
    getPath(file: FileInfo) {
        if (!file.path || file.path.length == 0)
            return '';
        return file.path.join(this.editSettings.pathSeparator);
    }
    
    setPath(file: FileInfo, path: string) {
        if (!path) {
            path ='';
        }
        
        var folders = path.split(this.editSettings.pathSeparator).filter(p => p && p.length > 0);
        file.path = folders;
    }

    private cancel() {
        this.state = 0;
    }
    
    startEdit() {
        this._outputFolders.combineLatest(this._settings, (outputFolders, settings) => ({outputFolders: outputFolders, settings: settings}))
            .subscribe(d => {
                this.rootFolders = d.outputFolders;
                this.editSettings = d.settings;
                this.editLink = Object.assign({}, this.newLink);
            });
    }
    
    getFolderPathByName(folder: string) {
        if (this.absolutePath) {
            var folderInfo = this.rootFolders.filter(f => f.name == folder).pop();
            return folderInfo ? folderInfo.path.join(this.editSettings.pathSeparator) : folder;
        } else {
            return folder;
        }
    }
    
    getFolderPath(folder: FolderInfo) {
        if (this.absolutePath) {
            return folder.path.join(this.editSettings.pathSeparator);
        } else {
            return folder.name;
        }
    }
    
    setRootFolder(rootFolder) {
        this.editLink.folder = rootFolder;
    }
    
    cancelEdit() {
        this.editLink = null;
    }
    
    saveEdit() {
        this.newLink = this.editLink;
        this.editLink = null;
    }

    link() {
        this.state = 3;
        setTimeout(function() {
            this.state = 0;
        }, 2);
    }

    ngOnInit() {
        this._settings = this._settingsService.settings();
        this._outputFolders = this._settingsService.outputFolders();
    }
}
