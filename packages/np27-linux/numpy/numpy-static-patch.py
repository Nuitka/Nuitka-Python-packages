Index: numpy/distutils/command/install_clib.py
IDEA additional info:
Subsystem: com.intellij.openapi.diff.impl.patch.CharsetEP
<+>UTF-8
===================================================================
diff --git a/numpy/distutils/command/install_clib.py b/numpy/distutils/command/install_clib.py
--- a/numpy/distutils/command/install_clib.py    (revision 3dec7099ce38cb189880f6f69df318f35ff9a5ea)
+++ b/numpy/distutils/command/install_clib.py    (date 1638937643652)
@@ -34,6 +34,8 @@
             source = os.path.join(build_dir, name)
             self.mkpath(target_dir)
             self.outfiles.append(self.copy_file(source, target_dir)[0])
+            if os.path.exists(source + '.link.json'):
+                self.outfiles.append(self.copy_file(source + '.link.json', target_dir)[0])

     def get_outputs(self):
         return self.outfiles
Index: numpy/distutils/command/build_ext.py
IDEA additional info:
Subsystem: com.intellij.openapi.diff.impl.patch.CharsetEP
<+>UTF-8
===================================================================
diff --git a/numpy/distutils/command/build_ext.py b/numpy/distutils/command/build_ext.py
--- a/numpy/distutils/command/build_ext.py    (revision 3dec7099ce38cb189880f6f69df318f35ff9a5ea)
+++ b/numpy/distutils/command/build_ext.py    (date 1638939198440)
@@ -5,6 +5,7 @@

 import os
 import subprocess
+import json
 from glob import glob

 from distutils.dep_util import newer_group
@@ -466,15 +467,20 @@
                     fcompiler, library_dirs,
                     unlinkable_fobjects)

-        linker(objects, ext_filename,
-               libraries=libraries,
-               library_dirs=library_dirs,
-               runtime_library_dirs=ext.runtime_library_dirs,
-               extra_postargs=extra_args,
-               export_symbols=self.get_export_symbols(ext),
-               debug=self.debug,
-               build_temp=self.build_temp,
-               target_lang=ext.language)
+        ext_filename = ext_filename.replace(".so", "")
+
+        self.compiler.create_static_lib(
+            objects, ext_filename, output_dir=os.path.abspath("."), debug=self.debug)
+
+        result_path = \
+            self.compiler.library_filename(ext_filename, output_dir=os.path.abspath("."))
+
+        with open(result_path + '.link.json', 'w') as f:
+            json.dump({
+                'libraries': self.get_libraries(ext),
+                'library_dirs': ext.library_dirs + ['lib'],
+                'runtime_library_dirs': ext.runtime_library_dirs,
+                'extra_postargs': extra_args}, f)

     def _add_dummy_mingwex_sym(self, c_sources):
         build_src = self.get_finalized_command("build_src").build_src
Index: numpy/core/setup.py
IDEA additional info:
Subsystem: com.intellij.openapi.diff.impl.patch.CharsetEP
<+>UTF-8
===================================================================
diff --git a/numpy/core/setup.py b/numpy/core/setup.py
--- a/numpy/core/setup.py    (revision 3dec7099ce38cb189880f6f69df318f35ff9a5ea)
+++ b/numpy/core/setup.py    (date 1638943041772)
@@ -709,9 +709,13 @@
                        join('src', 'common', 'npy_binsearch.h.src'),
                        join('src', 'npysort', 'binsearch.c.src'),
                        ]
-    config.add_library('npysort',
-                       sources=npysort_sources,
-                       include_dirs=[])
+    config.add_installed_library('npysort',
+                                 sources=npysort_sources,
+                                 install_dir='lib',
+                                 build_info={
+                                     'include_dirs': [],  # empty list required for creating npy_math_internal.h
+                                     'extra_compiler_args': (['/GL-'] if is_msvc else []),
+                                 })

     #######################################################################
     #                     multiarray_tests module                         #
