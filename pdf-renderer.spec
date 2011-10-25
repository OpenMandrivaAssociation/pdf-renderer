%define alternate_name PDFRenderer
%define cvs_version 2009_04_05
%define cvs_rel .%(echo %{cvs_version}|sed 's|_||g')cvs

Summary:        A 100% Java PDF renderer and viewer
Name:           pdf-renderer
Version:        0
Release:        4
License:        LGPLv2+
URL:            https://pdf-renderer.dev.java.net/
Group:          Development/Java
Source0:        https://pdf-renderer.dev.java.net/files/documents/6008/131974/%{alternate_name}-%{cvs_version}-src.zip
BuildRequires:  ant
BuildRequires:  java-rpmbuild
BuildRequires:  ant-apache-regexp
BuildRequires:  java-devel >= 0:1.6.0
BuildRequires:  jpackage-utils
BuildRequires:  ghostscript-fonts
BuildRequires:  unzip
BuildArch:      noarch
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Requires:       java
Requires:       jpackage-utils >= 1.5
Requires:       ghostscript-fonts
Provides:       %{alternate_name} == %{version}-%{release}

%description
The PDF Renderer is just what the name implies: an open source,
all Java library which renders PDF documents to the screen using 
Java2D. Typically this means drawing into a Swing panel, but it 
could also draw to other Graphics2D implementations. It could be 
used to draw on top of PDFs, share them over a network, convert 
PDFs to PNG images, or maybe even project PDFs into a 3D scene.

%package javadoc
Summary:        Javadoc for %{alternate_name}
Group:          Development/Java
Requires:       %{name} = %{version}-%{release}
Requires:       jpackage-utils

%description javadoc
API documentation for the %{alternate_name} package.

%prep
%setup -q -n %{alternate_name}-%{cvs_version}-src

# Remove preshipped binaries
find . -name "*.jar" -exec rm {} \;

# Fix encoding issues
find . -name "*.java" -exec native2ascii {} {} \;

# Remove preshipped fonts and ...
find . -name "*.pfb" -exec rm {} \;

# ... tell the program to use system-fonts instead.
# Script provided by Mamoru Tasaka:
# https://bugzilla.redhat.com/show_bug.cgi?id=466394#c4
# -------------------------------------------------------------
pushd src/com/sun/pdfview/font/res/
INPUT=BaseFonts.properties
OUTPUT=BaseFonts.properties.1
FONTDIR=%{_datadir}/fonts/default/Type1

rm -f $OUTPUT
cat $INPUT | while read line
 do
 newline=$line
 if echo $newline | grep -q 'file=.*pfb'
  then
  pfbname=$(echo $newline | sed -e 's|^.*file=||')
  newline=$(echo $newline | sed -e "s|file=|file=${FONTDIR}/|")
 elif echo $newline | grep -q 'length='
  then
  size=$(ls -al ${FONTDIR}/$pfbname | awk '{print $5}')
  newline=$(echo $newline | sed -e "s|length=.*|length=$size|")
 fi
 echo $newline >> $OUTPUT
done
mv -f $OUTPUT $INPUT
popd
# -------------------------------------------------------------

%build
%ant

%install
mkdir -p $RPM_BUILD_ROOT%{_javadir}
install -m 644 dist/%{alternate_name}.jar \
      $RPM_BUILD_ROOT%{_javadir}/%{name}.jar

# javadoc
mkdir -p $RPM_BUILD_ROOT%{_javadocdir}/%{name}
cp -pr dist/javadoc/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}

%files
%defattr(0644,root,root,0755)
%doc demos
%{_javadir}/%{name}.jar

%files javadoc
%defattr(0644,root,root,0755)
%{_javadocdir}/%{name}

# -----------------------------------------------------------------------------
