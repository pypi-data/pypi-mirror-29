// Scripted Forms -- Making GUIs easy for everyone on your team.
// Copyright (C) 2017 Simon Biggs

// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU Affero General Public License as published
// by the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version (the "AGPL-3.0+").

// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
// GNU Affero General Public License and the additional terms for more
// details.

// You should have received a copy of the GNU Affero General Public License
// along with this program. If not, see <http://www.gnu.org/licenses/>.

// ADDITIONAL TERMS are also included as allowed by Section 7 of the GNU
// Affrero General Public License. These aditional terms are Sections 1, 5,
// 6, 7, 8, and 9 from the Apache License, Version 2.0 (the "Apache-2.0")
// where all references to the definition "License" are instead defined to
// mean the AGPL-3.0+.

// You should have received a copy of the Apache-2.0 along with this
// program. If not, see <http://www.apache.org/licenses/LICENSE-2.0>.

// import { combineLatest } from 'rxjs/observable/combineLatest';

import { Injectable } from '@angular/core';

import {
  PromiseDelegate
} from '@phosphor/coreutils';

import {
  ServerConnection, Session
} from '@jupyterlab/services';

import { JupyterService } from './jupyter.service';
import { FileService } from './file.service';
import { FormService } from './form.service';
import { KernelService } from './kernel.service';
// import { VariableService } from './variable.service';

import {
  watchdogCode, watchdogWatchModeCode
} from './watchdog-code'

@Injectable()
export class WatchdogService {
  // formFirstPassComplete = new PromiseDelegate<void>();
  everythingIdle = new PromiseDelegate<void>();

  constructor(
    private myFileService: FileService,
    private myJupyterService: JupyterService,
    private myFormService: FormService,
    // private myVariableService: VariableService,
    private myKernelService: KernelService
  ) { }

  // "kernelStatus !== 'idle' || formStatus !== 'ready' || variableStatus !== 'idle'"

  // runWatchdogAfterFormReady() {
  //   let subscription = combineLatest(
  //     this.myFormService.formStatus,
  //     this.myVariableService.variableStatus,
  //     this.myKernelService.kernelStatus).subscribe(([formStatus, variableStatus, kernelStatus]) => {
  //       if ((formStatus === 'ready') && (variableStatus === 'idle') && (kernelStatus === 'idle')) {
  //         subscription.unsubscribe()
  //         this.runWatchdog()
  //       }
  //     })

  //   // this.formFirstPassComplete.promise.then(() => {
  //   //   this.runWatchdog()
  //   // })
  // }


  runDevModeWatchdog() {
    let sessionReady = new PromiseDelegate<Session.ISession>();

    const path = 'scriptedforms_watchdog_development_mode_kernel'
    const settings = ServerConnection.makeSettings({});
    const startNewOptions = {
      kernelName: 'python3',
      serverSettings: settings,
      path: path
    };
  
    this.myJupyterService.serviceManager.sessions.findByPath(path).then(model => {
      Session.connectTo(model, settings).then(session => {
        sessionReady.resolve(session)
      });
    }).catch(() => {
      Session.startNew(startNewOptions).then(session => {
        session.kernel.requestExecute({code: watchdogWatchModeCode})
        sessionReady.resolve(session)
      });
    });

    sessionReady.promise.then(session => {
      session.iopubMessage.connect((sender, msg) => {
        if (msg.content.text) {
          let content = String(msg.content.text).trim()
          let files = content.split("\n")
          console.log(files)
          location.reload(true)
        }
      })
    })
  }



  runWatchdog() {
    if (process.env.development) {
      this.runDevModeWatchdog()
    }

    const path = 'scriptedforms_watchdog_kernel'
    const settings = ServerConnection.makeSettings({});
    const startNewOptions = {
      kernelName: 'python3',
      serverSettings: settings,
      path: path
    };
  
    this.myJupyterService.serviceManager.sessions.findByPath(path).then(model => {
      Session.connectTo(model, settings).then(session => {
        this.watchdogFormUpdate(session)
      });
    }).catch(() => {
      Session.startNew(startNewOptions).then(session => {
        session.kernel.requestExecute({code: watchdogCode})
        this.watchdogFormUpdate(session)
      });
    });
  }

  watchdogFormUpdate(session: Session.ISession) {
    session.iopubMessage.connect((sender, msg) => {
      if (msg.content.text) {
        let content = String(msg.content.text).trim()
        let files = content.split("\n")
        console.log(files)
        let path = this.myFileService.path.getValue()
        let sessionId = this.myFormService.currentFormSessionId
        let match = files.some(item => {
          return (item.replace('\\', '/') === path) || (item.includes('goutputstream'))
        })
        if (match) {
          this.myKernelService.sessionStore[this.myKernelService.currentSession].isNewSession = false
          this.myFileService.loadFileContents(path, sessionId)
        }
      }
    })
  }
}