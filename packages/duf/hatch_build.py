import os
import subprocess
import urllib
import urllib.request

from hatchling.builders.hooks.plugin.interface import BuildHookInterface


class ABCDEFGHIJIKLBuildHook(BuildHookInterface):
    PLUGIN_NAME = 'custom'

    @property
    def dotnet_path(self):
        return os.path.join(self.root, ".dotnet")

    @property
    def dotnet_install_script(self):
        return os.path.join(self.dotnet_path, "dotnet-install.sh")

    @property
    def dotnet_exe(self):
        return os.path.join(self.dotnet_path, "dotnet.exe")

    @property
    def simple_duf_csharp_project_dir(self):
        return os.path.join(self.root, "csharp", "SimpleDuf")

    @property
    def simple_duf_csharp_project_file(self):
        return os.path.join(self.simple_duf_csharp_project_dir, "duf.csproj")

    @property
    def simple_duf_output_bin(self):
        return os.path.join(self.simple_duf_csharp_project_dir, "bin")

    def initialize(self, version: str, build_data) -> None:
        print('+++ initialize')
        # print(version)
        # print(build_data)
        # print(self.config)


        self._install_local_dotnet_sdk()
        self._build_simple_duf()
        # project_root = Path(self.root)
        # sdk_version: str = cfg.get("sdk_version") or "8.0.401"
        # dotnet_cmd, env = self._ensure_dotnet(project_root, sdk_version)
        #
        # for p in projects:
        #     self._build_one_project(project_root, dotnet_cmd, env, p)





    def _install_local_dotnet_sdk(self):
        print('+++ download sdk')

        install_source = "https://dot.net/v1/dotnet-install.ps1"

        dotnet_path = os.path.join(self.root, ".dotnet")
        dotnet_install_script = os.path.join(dotnet_path, "dotnet-install.ps1")

        os.makedirs(dotnet_path, exist_ok=True)

        urllib.request.urlretrieve(install_source, dotnet_install_script)

        cmd = [
            "powershell",
            "-ExecutionPolicy",
            "Bypass",
            "-NoLogo",
            "-NoProfile",
            "-File",
            dotnet_install_script,
            # "-Version",
            # sdk_version,
            "-InstallDir",
            dotnet_path,
            # "-NoPath",
        ]

        print(f'_install_local_dotnet_sdk: trying to run cmd {cmd}')

        subprocess.run(cmd)

    def _build_simple_duf(self):
        cmd = [
            self.dotnet_exe,
            "build",
            "--configuration",
            "Release",
            "--output",
            self.simple_duf_output_bin,
            self.simple_duf_csharp_project_file
        ]

        print(f'_build_simple_duf: trying to run cmd {cmd}')

        subprocess.run(cmd)


        # ------------- dotnet helpers -------------
    #
    # def _ensure_dotnet(self, project_root: Path, sdk_version: str) -> tuple[str, Dict[str, str]]:
    #     env = os.environ.copy()
    #     env.setdefault("DOTNET_NOLOGO", "1")
    #     env.setdefault("DOTNET_SKIP_FIRST_TIME_EXPERIENCE", "1")
    #     env.setdefault("DOTNET_CLI_TELEMETRY_OPTOUT", "1")
    #
    #     # Prefer an existing dotnet on PATH
    #     try:
    #         existing = subprocess.check_output(["dotnet", "--version"], text=True).strip()
    #         self.app.display_info(f"[dotnet] Using system SDK: {existing}")
    #         return "dotnet", env
    #     except Exception:
    #         pass
    #
    #     # Install a private SDK into ./.dotnet
    #     install_dir = project_root / ".dotnet"
    #     install_dir.mkdir(parents=True, exist_ok=True)
    #
    #     is_windows = platform.system() == "Windows"
    #     script_url = "https://dot.net/v1/dotnet-install.ps1" if is_windows else "https://dot.net/v1/dotnet-install.sh"
    #     script_path = install_dir / ("dotnet-install.ps1" if is_windows else "dotnet-install.sh")
    #
    #     self.app.display_info(f"[dotnet] Downloading {script_url}")
    #     with urllib.request.urlopen(script_url) as r, open(script_path, "wb") as f:
    #         f.write(r.read())
    #     if not is_windows:
    #         script_path.chmod(0o755)
    #
    #     self.app.display_info(f"[dotnet] Installing SDK {sdk_version} into {install_dir}")
    #     if is_windows:
    #         cmd = [
    #             "powershell",
    #             "-ExecutionPolicy",
    #             "Bypass",
    #             "-NoLogo",
    #             "-NoProfile",
    #             "-File",
    #             str(script_path),
    #             "-Version",
    #             sdk_version,
    #             "-InstallDir",
    #             str(install_dir),
    #             "-NoPath",
    #         ]
    #     else:
    #         cmd = [str(script_path), "--version", sdk_version, "--install-dir", str(install_dir), "--no-path"]
    #     self._run(cmd, cwd=project_root, env=env)
    #
    #     dotnet_bin = install_dir / ("dotnet.exe" if is_windows else "dotnet")
    #     if not dotnet_bin.exists():
    #         raise RuntimeError("dotnet install did not produce an executable")
    #
    #     env["DOTNET_ROOT"] = str(install_dir)
    #     env["PATH"] = f"{install_dir}{os.pathsep}{env.get('PATH', '')}"
    #     return str(dotnet_bin), env
    #
    # def _build_one_project(
    #         self,
    #         project_root: Path,
    #         dotnet_cmd: str,
    #         env: Dict[str, str],
    #         cfg: Dict[str, Any],
    # ) -> None:
    #     """
    #     cfg:
    #       csproj (str, required)                  - path to the .csproj (relative to repo root)
    #       tfm (str, default 'net472')             - TargetFramework moniker
    #       configuration (str, default 'Release')  - Build configuration
    #       dest (str, required)                    - directory inside your Python package to receive the DLL
    #       assembly_name (str, optional)           - override DLL name; default resolves from csproj
    #     """
    #     csproj_rel = cfg.get("csproj")
    #     if not csproj_rel:
    #         raise ValueError("Missing 'csproj' in dotnet project config")
    #     csproj = (project_root / csproj_rel).resolve()
    #     if not csproj.exists():
    #         raise FileNotFoundError(f".NET project file not found: {csproj}")
    #
    #     tfm = cfg.get("tfm") or "net472"
    #     configuration = cfg.get("configuration") or "Release"
    #     dest_rel = cfg.get("dest")
    #     if not dest_rel:
    #         raise ValueError("Missing 'dest' in dotnet project config")
    #     dest_dir = (project_root / dest_rel).resolve()
    #     dest_dir.mkdir(parents=True, exist_ok=True)
    #
    #     msbuild_props = [
    #         f"-p:Configuration={configuration}",
    #         "-p:ContinuousIntegrationBuild=true",
    #         "-p:EnableFrameworkPathOverride=true",
    #     ]
    #
    #     self._run([dotnet_cmd, "restore", str(csproj)] + msbuild_props, cwd=project_root, env=env)
    #     self._run(
    #         [dotnet_cmd, "build", str(csproj), "-c", configuration, "-v", "minimal", "-nologo"] + msbuild_props,
    #         cwd=project_root,
    #         env=env,
    #     )
    #
    #     asm_name = cfg.get("assembly_name") or self._assembly_name_from_csproj(csproj)
    #     out_dir = csproj.parent / "bin" / configuration / tfm
    #     dll = out_dir / f"{asm_name}.dll"
    #     if not dll.exists():
    #         dlls = list(out_dir.glob("*.dll"))
    #         if not dlls:
    #             raise FileNotFoundError(f"No DLL found under {out_dir}")
    #         dll = dlls[0]
    #
    #     dest_path = dest_dir / dll.name
    #     shutil.copy2(dll, dest_path)
    #     self.app.display_info(f"[dotnet] Copied {dll} -> {dest_path}")
    #
    # def _assembly_name_from_csproj(self, csproj: Path) -> str:
    #     try:
    #         import xml.etree.ElementTree as ET
    #
    #         root = ET.parse(csproj).getroot()
    #         tags = ("AssemblyName", "{http://schemas.microsoft.com/developer/msbuild/2003}AssemblyName")
    #         for tag in tags:
    #             el = root.find(f".//{tag}")
    #             if el is not None and el.text:
    #                 return el.text.strip()
    #     except Exception:
    #         pass
    #     return csproj.stem
    #
    # def _run(self, cmd: List[str], cwd: Optional[Path] = None, env: Optional[Dict[str, str]] = None):
    #     self.app.display_info(f"[dotnet] Running: {' '.join(cmd)}")
    #     subprocess.run(cmd, cwd=cwd, env=env, check=True)


