import { Injectable } from "@angular/core";
import { Http }       from "@angular/http";
import { Observable } from "rxjs"
import "rxjs/add/operator/map";
import "rxjs/add/operator/share";

export interface Settings {
    pathSeparator: string
}

export interface FolderInfo {
    name: string;
    path: string[];
}

@Injectable()
export class SettingsService {
    private _settings: Observable<Settings>;
    private _inputFolders: Observable<FolderInfo[]>;
    private _outputFolders: Observable<FolderInfo[]>;
    
    constructor(private _http: Http) {
        this._settings = this._http
            .get("api/settings")
            .map(r => <Settings> r.json())
            .share();
        this._inputFolders = this._http
            .get("api/settings/input-folders")
            .map(r => <FolderInfo[]> r.json())
            .share();
        this._outputFolders = this._http
            .get("api/settings/output-folders")
            .map(r => <FolderInfo[]> r.json())
            .share();
    }
    
    settings() : Observable<Settings> {
        return this._settings;
    }
    
    inputFolders() : Observable<FolderInfo[]> {
        return this._inputFolders;
    }
    
    outputFolders() : Observable<FolderInfo[]> {
        return this._outputFolders;
    }
}
