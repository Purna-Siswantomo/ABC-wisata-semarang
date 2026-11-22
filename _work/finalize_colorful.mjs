import path from 'node:path';
import fs from 'node:fs/promises';
import {pathToFileURL} from 'node:url';
const workspaceDir=path.resolve('Swarm Intelligence/Project ABC Wisata Semarang');
const skill='C:/Users/Purna Siswantomo/.codex/plugins/cache/openai-primary-runtime/presentations/26.1118.11504/skills/presentations';
const {finalizePresentation}=await import(pathToFileURL(path.join(skill,'container_tools/artifact_tool_utils.mjs')).href);
const runtime='C:/Program Files/WindowsApps/OpenAI.CodexPrimaryRuntime.v26-1118-904-0_26.1118.904.0_x64__3k8sg7r9htsxt/dependencies';
await fs.mkdir(path.join(workspaceDir,'presentasi'),{recursive:true});
const result=await finalizePresentation({workspaceDir,
 candidatePath:path.join(workspaceDir,'_work/candidate_colorful.pptx'),
 finalPath:path.join(workspaceDir,'presentasi/Presentasi_ABC_Wisata_Semarang_Colorful.pptx'),
 explicitTotalSlideCount:10,
 pythonExecutable:path.join(runtime,'python/python.exe'),
 integrityValidatorPath:path.join(skill,'container_tools/inspect_presentation_package_integrity.py'),
 layoutValidatorPath:path.join(skill,'container_tools/inspect_presentation_layout_geometry.py'),
 layoutArgs:['--expected-slide-size-emu','12192000,6858000','--validate-bullet-geometry','--validate-heading-fit','--require-native-table-slide','8'],
 requiredNativeTableOwnerSlides:[8],requiredNativeChartOwnerSlides:[],
 fontPolicy:{basis:'design',families:['Arial']},
 verifyArtifactToolImport:true,
 receiptPath:path.join(workspaceDir,'_work/presentation_colorful.validation.json')});
console.log(JSON.stringify(result));
