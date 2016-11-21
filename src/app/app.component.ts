import { Component }       from "@angular/core";

@Component({
    selector: 'hl-app',
    template: `
    <nav class="navbar navbar-inverse navbar-fixed-top">
        <div class="container-fluid">
            <div class="navbar-header">
                <a class="navbar-brand" href="/">Hard Linker</a>
            </div>
            <div id="navbar" class="collapse navbar-collapse">
                <ul class="nav navbar-nav">
                    <li><a routerLink="/browse">Browse</a></li>
                    <li><a routerLink="/settings">Settings</a></li>
                </ul>
            </div>
        </div>
    </nav>

    <div class="container-fluid">

        <div class="hard-linker">
            <router-outlet></router-outlet>
        </div>

    </div>    
    `,
})
export class AppComponent {
}
