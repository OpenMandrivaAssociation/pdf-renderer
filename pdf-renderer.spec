%{?_javapackages_macros:%_javapackages_macros}
%global alternate_name PDFRenderer
%global svn_date 20110310
%global svn_version 128svn

Summary:        A 100% Java PDF renderer and viewer
Name:           pdf-renderer
Version:        0
Release:        0.15.%{svn_version}.%{svn_date}.0%{?dist}
#src/com/sun/pdfview/decode/CCITTFaxDecoder.java under a BSD-alike License
#src/com/sun/pdfview/font/ttf/resource/glyphlist.txt and src/com/sun/pdfview/font/ttf/AdobeGlyphList.java
#are under Adobe Glyph List License
License:        LGPLv2+ and MIT and BSD
URL:            https://pdf-renderer.dev.java.net/

Source0:        %{name}-%{svn_version}-%{svn_date}.tar.bz2
# To fetch the source code
Source1:        %{name}-snapshot.sh
BuildRequires:  ant
BuildRequires:  ant-apache-regexp
BuildRequires:  java-devel >= 1.7
BuildRequires:  jpackage-utils
BuildRequires:  urw-fonts
BuildArch:      noarch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:       java >= 1.7
Requires:       jpackage-utils >= 1.5
Requires:       urw-fonts
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

Requires:       %{name} = %{version}-%{release}
Requires:       jpackage-utils

%description javadoc
API documentation for the %{alternate_name} package.

%prep
%setup -q -n %{name}-%{svn_version}-%{svn_date}

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
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_javadir}
install -m 644 dist/%{alternate_name}.jar \
      $RPM_BUILD_ROOT%{_javadir}/%{name}.jar

# javadoc
mkdir -p $RPM_BUILD_ROOT%{_javadocdir}/%{name}
cp -pr dist/javadoc/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc demos
%{_javadir}/%{name}.jar

%files javadoc
%defattr(-,root,root,-)
%{_javadocdir}/%{name}

# -----------------------------------------------------------------------------

%changelog
* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0-0.14.128svn.20110310
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0-0.13.128svn.20110310
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Nov 06 2012 Caolán McNamara <caolanm@redhat.com> - 0-0.12.128svn.20110310
- src/com/sun/pdfview/decode/CCITTFaxDecoder.java BSD-alike License

* Fri Nov 02 2012 Caolán McNamara <caolanm@redhat.com> - 0-0.11.128svn.20110310
- src/com/sun/pdfview/font/ttf/resource/glyphlist.txt and src/com/sun/pdfview/font/ttf/AdobeGlyphList.java
  are under Adobe Glyph List License

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0-0.10.128svn.20110310
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0-0.9.128svn.20110310
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Mar 10 2011 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> 0-0.8.128svn.20110310
- New svn checkout
- Drop gcj as per new guidelines

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0-0.7.20090405cvs
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0-0.6.20090405cvs
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Apr 11 2009 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> 0-0.5.20090405cvs
- New cvs checkout
- Raise minimum java requirement

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0-0.4.20090118cvs.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Jan 21 2009 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> 0-0.4.20090118cvs
- New cvs checkout

* Sat Oct 11 2008 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> 0-0.3.20081005cvs
- The license is changed to LGPLv2+.
- Fixed sizes of the font files on src/com/sun/pdfview/font/res/BaseFonts.properties
- BuildRequired urw-fonts

* Fri Oct 10 2008 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> 0-0.2.20081005cvs
- Removed pre-shipped fonts and told the program to use system-wide urw-fonts.
- The license is changed to LGPLv2+ and GPL+.

* Thu Oct 09 2008 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> 0-0.1.20081005cvs
- Initial Release
