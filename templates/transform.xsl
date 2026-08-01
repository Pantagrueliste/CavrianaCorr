<?xml version="1.0" encoding="UTF-8"?>
<!-- XSLT for converting TEI letters to Docusaurus Markdown -->
<xsl:stylesheet
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:tei="http://www.tei-c.org/ns/1.0"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:cav="https://github.com/Pantagrueliste/CavrianaCorr"
    exclude-result-prefixes="tei xs cav"
    version="2.0">

  <!-- Produce text output (not HTML), but we will embed raw HTML tags
       by escaping them and using disable-output-escaping. -->
  <xsl:output method="text" encoding="UTF-8"/>
  <xsl:strip-space elements="tei:*"/>

  <!-- Escape a value destined for an HTML attribute. The output method is
       text, so nothing is escaped for us. -->
  <xsl:function name="cav:attr" as="xs:string">
    <xsl:param name="v"/>
    <xsl:sequence select="replace(replace(replace(string($v), '&amp;', '&amp;amp;'), '&lt;', '&amp;lt;'), '&quot;', '&amp;quot;')"/>
  </xsl:function>

  <!-- Escape text destined for the page body. The pages are compiled as MDX,
       where a bare { opens an expression and < opens a tag: both compile
       silently and then fail at render time. No transcription contains these
       characters today; this keeps it that way if one ever does. -->
  <xsl:function name="cav:mdx" as="xs:string">
    <xsl:param name="v"/>
    <xsl:sequence select="replace(replace(replace(string($v), '\{', '\\{'), '\}', '\\}'), '&lt;', '&amp;lt;')"/>
  </xsl:function>

  <!-- 1)  Entry point: collect entire text, then strip spaces before punctuation. -->
  <xsl:template match="/">
    <xsl:variable name="rawOutput">
      <xsl:apply-templates select="tei:TEI"/>
    </xsl:variable>
    <!-- Drop the space a <choice> leaves before punctuation. Only spaces and
         tabs: swallowing newlines would pull punctuation onto the line of a
         closing block tag, which MDX rejects. -->
    <xsl:value-of select="replace($rawOutput, '[ \t]+([,;\.])', '$1')"/>
  </xsl:template>

  <!-- 2) Process root <TEI> to output front matter, then apply templates to the text. -->
  <xsl:template match="tei:TEI">
    <xsl:variable name="msId" select="tei:teiHeader/tei:fileDesc/tei:sourceDesc/tei:msDesc/tei:msIdentifier"/>
    <xsl:variable name="locusFrom" select="tei:teiHeader/tei:fileDesc/tei:sourceDesc/tei:msDesc/tei:msContents/tei:msItem/tei:locus/@from"/>
    <xsl:variable name="locusTo"   select="tei:teiHeader/tei:fileDesc/tei:sourceDesc/tei:msDesc/tei:msContents/tei:msItem/tei:locus/@to"/>

    <!-- Archive reference. Every repository name in the corpus already names
         its city ("Archivio di Stato di Firenze"), so msIdentifier/placeName
         is not repeated here. Missing parts are skipped rather than producing
         empty ', ,' runs; a single-folio range collapses to 'fol. N'. -->
    <xsl:variable name="locusPart" as="xs:string"
      select="if (string($locusFrom) ne '' and string($locusTo) ne '' and string($locusFrom) ne string($locusTo))
              then concat('fols. ', $locusFrom, '-', $locusTo)
              else if (string($locusFrom) ne '') then concat('fol. ', $locusFrom)
              else ''"/>
    <xsl:variable name="archiveRef" as="xs:string"
      select="string-join((
                normalize-space($msId/tei:repository)[. ne ''],
                normalize-space($msId/tei:collection)[. ne ''],
                normalize-space($msId/tei:idno)[. ne ''],
                $locusPart[. ne '']
              ), ', ')"/>

    <!-- YAML-like front matter for Markdown -->
    <xsl:text>---&#10;</xsl:text>

    <xsl:variable name="sentDate" select="tei:teiHeader/tei:profileDesc/tei:correspDesc/tei:correspAction[@type='sent']/tei:date"/>
    <xsl:variable name="dateValue" select="if ($sentDate/@when) then $sentDate/@when else if ($sentDate/@notBefore) then $sentDate/@notBefore else ''"/>

    <xsl:text>title: "</xsl:text>
    <xsl:value-of select="$dateValue"/>
    <xsl:text>"&#10;</xsl:text>

    <xsl:text>expeditor: "</xsl:text>
    <xsl:value-of select="normalize-space(tei:teiHeader/tei:profileDesc/tei:correspDesc/tei:correspAction[@type='sent']/tei:persName)"/>
    <xsl:text>"&#10;</xsl:text>

    <xsl:text>addressee: "</xsl:text>
    <xsl:value-of select="normalize-space(tei:teiHeader/tei:profileDesc/tei:correspDesc/tei:correspAction[@type='received']/tei:persName)"/>
    <xsl:text>"&#10;</xsl:text>

    <xsl:text>date: "</xsl:text>
    <xsl:value-of select="$dateValue"/>
    <xsl:text>"&#10;</xsl:text>

    <xsl:text>placeOfOrigin: "</xsl:text>
    <xsl:value-of select="normalize-space(tei:teiHeader/tei:profileDesc/tei:correspDesc/tei:correspAction[@type='sent']/tei:placeName)"/>
    <xsl:text>"&#10;</xsl:text>

    <xsl:text>archiveRef: "</xsl:text>
    <xsl:value-of select="$archiveRef"/>
    <xsl:text>"&#10;</xsl:text>

    <xsl:if test="tei:text//tei:seg[@type='cipher']">
      <xsl:text>hasCipher: true&#10;</xsl:text>
    </xsl:if>

    <xsl:text>---&#10;</xsl:text>
    <xsl:text>&#10;</xsl:text>

    <!-- Visible metadata block -->
    <xsl:variable name="sender"       select="tei:teiHeader/tei:profileDesc/tei:correspDesc/tei:correspAction[@type='sent']/tei:persName"/>
    <xsl:variable name="senderPlace"  select="tei:teiHeader/tei:profileDesc/tei:correspDesc/tei:correspAction[@type='sent']/tei:placeName"/>
    <xsl:variable name="sendDate"     select="tei:teiHeader/tei:profileDesc/tei:correspDesc/tei:correspAction[@type='sent']/tei:date"/>
    <xsl:variable name="receiver"     select="tei:teiHeader/tei:profileDesc/tei:correspDesc/tei:correspAction[@type='received']/tei:persName"/>
    <xsl:variable name="receiverPlace" select="tei:teiHeader/tei:profileDesc/tei:correspDesc/tei:correspAction[@type='received']/tei:placeName"/>
    <xsl:variable name="receivedDate" select="tei:teiHeader/tei:profileDesc/tei:correspDesc/tei:correspAction[@type='received']/tei:date"/>
    <xsl:variable name="summary"      select="tei:teiHeader/tei:fileDesc/tei:sourceDesc/tei:msDesc/tei:msContents/tei:msItem/tei:note[@type='summary']"/>
    <!-- A pseudonymous sender is encoded either as a note in the msItem or,
         more usually, as persName/@type='alias' on the sent action. -->
    <xsl:variable name="isAlias" as="xs:boolean"
      select="exists(tei:teiHeader/tei:fileDesc/tei:sourceDesc/tei:msDesc/tei:msContents/tei:msItem/tei:note[@type='pseudonym'])
              or $sender/@type = 'alias'"/>

    <xsl:text disable-output-escaping="yes">&lt;div class="letter-metadata"&gt;&#10;</xsl:text>
    <xsl:text>&#10;</xsl:text>
    <xsl:text>| | |&#10;</xsl:text>
    <xsl:text>|---|---|&#10;</xsl:text>

    <xsl:text>| **From** | </xsl:text>
    <xsl:value-of select="normalize-space($sender)"/>
    <xsl:if test="$isAlias">
      <xsl:text> (pseudonym)</xsl:text>
    </xsl:if>
    <xsl:if test="normalize-space($senderPlace) != ''">
      <xsl:text>, </xsl:text>
      <xsl:value-of select="normalize-space($senderPlace)"/>
    </xsl:if>
    <xsl:text> |&#10;</xsl:text>

    <xsl:text>| **To** | </xsl:text>
    <xsl:value-of select="if (normalize-space($receiver) ne '') then normalize-space($receiver) else 'unknown'"/>
    <xsl:if test="normalize-space($receiverPlace) != ''">
      <xsl:text>, </xsl:text>
      <xsl:value-of select="normalize-space($receiverPlace)"/>
    </xsl:if>
    <xsl:text> |&#10;</xsl:text>

    <xsl:text>| **Date** | </xsl:text>
    <xsl:value-of select="normalize-space($sendDate)"/>
    <xsl:text> |&#10;</xsl:text>

    <xsl:if test="$receivedDate">
      <xsl:text>| **Received** | </xsl:text>
      <xsl:value-of select="if (normalize-space($receivedDate) ne '') then normalize-space($receivedDate) else string($receivedDate/@when)"/>
      <xsl:text> |&#10;</xsl:text>
    </xsl:if>

    <xsl:text>| **Archive** | </xsl:text>
    <xsl:value-of select="$archiveRef"/>
    <xsl:text> |&#10;</xsl:text>

    <!-- Scribal hands. Eight letters are written in more than one hand, and
         several are copies or use a disguised hand — worth stating up front
         in an espionage correspondence. -->
    <xsl:variable name="hands" select="tei:teiHeader/tei:fileDesc/tei:sourceDesc/tei:msDesc/tei:physDesc/tei:handDesc/tei:handNote"/>
    <xsl:if test="$hands[normalize-space(.) != '']">
      <xsl:text>| **</xsl:text>
      <xsl:value-of select="if (count($hands) > 1) then 'Hands' else 'Hand'"/>
      <xsl:text>** | </xsl:text>
      <xsl:value-of select="cav:mdx(string-join($hands[normalize-space(.) != '']/normalize-space(.), '; '))"/>
      <xsl:text> |&#10;</xsl:text>
    </xsl:if>

    <!-- Suggested citation. The concept DOI always resolves to the latest
         version, so no access date is needed. -->
    <xsl:variable name="editor" select="tei:teiHeader/tei:fileDesc/tei:titleStmt/tei:editor"/>
    <xsl:variable name="letterTitle" select="tei:teiHeader/tei:fileDesc/tei:titleStmt/tei:title"/>
    <xsl:text>| **Cite as** | </xsl:text>
    <xsl:value-of select="normalize-space($editor)"/>
    <xsl:text> (ed.), "</xsl:text>
    <xsl:value-of select="cav:mdx(normalize-space($letterTitle))"/>
    <xsl:text>," in *Filippo Cavriana: The Secret Correspondence*, https://doi.org/10.5281/zenodo.8224585 |&#10;</xsl:text>

    <xsl:text>&#10;</xsl:text>
    <xsl:text disable-output-escaping="yes">&lt;/div&gt;&#10;</xsl:text>
    <xsl:text>&#10;</xsl:text>

    <!-- The scholarly abstract, as prose. It averages 313 characters and runs
         to nearly 2,000, which a two-column table cell cannot carry. Emitted
         through the templates so the people and places it names are linked
         like those in the transcription. -->
    <xsl:if test="$summary[normalize-space(.) != '']">
      <xsl:text disable-output-escaping="yes">&lt;div class="letter-summary"&gt;&#10;&#10;</xsl:text>
      <xsl:apply-templates select="$summary/node()"/>
      <xsl:text>&#10;&#10;</xsl:text>
      <xsl:text disable-output-escaping="yes">&lt;/div&gt;&#10;&#10;</xsl:text>
    </xsl:if>

    <!-- Cipher apparatus summary, on the letters that carry cipher. -->
    <xsl:variable name="ciphers" select="tei:text//tei:seg[@type='cipher']"/>
    <xsl:if test="$ciphers">
      <xsl:variable name="solved"
        select="count($ciphers[@xml:id and //tei:add[@type='decipher'][substring-after(@corresp,'#') = current()//tei:seg/@xml:id]])"/>
      <xsl:value-of disable-output-escaping="yes"
        select="concat('&lt;CipherNote total=&quot;', count($ciphers),
                       '&quot; solved=&quot;',
                       count(tei:text//tei:add[@type='decipher']) + count(tei:text//tei:supplied[@reason='deciphered']),
                       '&quot;/&gt;&#10;&#10;')"/>
    </xsl:if>

    <!-- Editorial statement. Set as a colophon rather than an alert: this is
         a standing statement about the edition's progress, not a warning. -->
    <xsl:text disable-output-escaping="yes">&lt;p class="editorial-notice"&gt;&lt;span&gt;Editorial notice&lt;/span&gt;This is a staged edition; the first stage (1566–1574) is not yet complete.&lt;/p&gt;&#10;</xsl:text>
    <xsl:text>&#10;</xsl:text>

    <!-- Now apply templates to the text body -->
    <xsl:apply-templates select="tei:text"/>
  </xsl:template>

  <!-- 3) <text> just applies recursively. -->
  <xsl:template match="tei:text">
    <xsl:apply-templates/>
  </xsl:template>

  <!-- 4) Page breaks. -->
  <xsl:template match="tei:pb">
    <xsl:text>&#10;**[fol. </xsl:text>
    <xsl:value-of select="@n"/>
    <xsl:text>]**&#10;&#10;</xsl:text>
  </xsl:template>

  <!-- 5) Line breaks: preserve original line breaks.
       break="no" means the word is split across lines, so add a hyphen. -->
  <!-- A line break inside an inline wrapper must not start a new output line:
       MDX would read the <br/> as an HTML block and leave the wrapper open. -->
  <xsl:template match="tei:lb[ancestor::tei:persName | ancestor::tei:placeName]" priority="2">
    <xsl:if test="@break = 'no'">
      <xsl:text>-</xsl:text>
    </xsl:if>
    <xsl:text disable-output-escaping="yes">&lt;br/&gt;</xsl:text>
  </xsl:template>
  <xsl:template match="tei:lb[@break='no']">
    <xsl:text disable-output-escaping="yes">-&lt;br/&gt;&#10;</xsl:text>
  </xsl:template>
  <xsl:template match="tei:lb">
    <xsl:text disable-output-escaping="yes">&lt;br/&gt;&#10;</xsl:text>
  </xsl:template>

  <!-- 6) Paragraph-like elements. The opener, closer and postscript are the
       formal architecture of a diplomatic letter, so they are wrapped rather
       than run together with the body. -->
  <xsl:template match="tei:p">
    <xsl:apply-templates/>
    <xsl:text>&#10;&#10;</xsl:text>
  </xsl:template>

  <!-- Block wrappers. These must be separated from their content by blank
       lines: the transcription is full of <br/> at the start of a line, which
       MDX reads as an HTML block, and an inline wrapper spanning such a line
       would be left unclosed. -->
  <xsl:template match="tei:opener | tei:closer | tei:postscript">
    <xsl:value-of disable-output-escaping="yes"
      select="concat('&#10;&#10;&lt;div class=&quot;letter-', local-name(), '&quot;&gt;&#10;&#10;')"/>
    <xsl:apply-templates/>
    <xsl:text>&#10;&#10;</xsl:text>
    <xsl:text disable-output-escaping="yes">&lt;/div&gt;&#10;&#10;</xsl:text>
  </xsl:template>

  <!-- 6b) Parts of the epistolary frame: the date and place of writing, the
       salutation, the subscription, and the address. None of these had a
       template, so they ran together as undifferentiated prose. -->
  <xsl:template match="tei:dateline | tei:salute | tei:signed | tei:address">
    <xsl:value-of disable-output-escaping="yes"
      select="concat('&#10;&#10;&lt;div class=&quot;', local-name(), '&quot;&gt;&#10;&#10;')"/>
    <xsl:apply-templates/>
    <xsl:text>&#10;&#10;</xsl:text>
    <xsl:text disable-output-escaping="yes">&lt;/div&gt;&#10;&#10;</xsl:text>
  </xsl:template>

  <!-- 7) persName/placeName. Names carrying a resolvable @ref become <Ent>,
       a component that looks the record up in the authority dataset and
       links to the index. Names without one are processed for their
       children, so that a nested <choice> still resolves to one reading
       rather than concatenating abbr and expan. -->
  <xsl:template match="tei:persName[@ref][@ref != '#'] | tei:placeName[@ref][@ref != '#']">
    <xsl:value-of disable-output-escaping="yes"
      select="concat('&lt;Ent k=&quot;',
                     if (self::tei:persName) then 'p' else 'l',
                     '&quot; id=&quot;', cav:attr(substring-after(@ref, '#')), '&quot;&gt;')"/>
    <xsl:apply-templates/>
    <xsl:text disable-output-escaping="yes">&lt;/Ent&gt;</xsl:text>
  </xsl:template>

  <xsl:template match="tei:persName | tei:placeName">
    <xsl:apply-templates/>
  </xsl:template>

  <!-- 8) <choice>: emit BOTH readings so the site can offer a diplomatic
       view. The expansion is shown by default and the manuscript's own
       abbreviation is revealed by the reader's view setting; only one of
       the two is ever displayed, so copied text stays clean.
       sic/corr and orig/reg keep the editorial reading only. -->
  <xsl:template match="tei:choice[tei:abbr][tei:expan]">
    <xsl:text disable-output-escaping="yes">&lt;span class="expan"&gt;</xsl:text>
    <xsl:apply-templates select="tei:expan"/>
    <xsl:text disable-output-escaping="yes">&lt;/span&gt;&lt;span class="abbr"&gt;</xsl:text>
    <xsl:apply-templates select="tei:abbr"/>
    <xsl:text disable-output-escaping="yes">&lt;/span&gt; </xsl:text>
  </xsl:template>

  <xsl:template match="tei:choice">
    <xsl:apply-templates select="(tei:expan, tei:corr, tei:reg, *[1])[1]"/>
    <xsl:text> </xsl:text>
  </xsl:template>

  <!-- 9) UNCLEAR words -->
  <xsl:template match="tei:unclear">
    <xsl:text disable-output-escaping="yes">&lt;span class="unclear"&gt;</xsl:text>
    <xsl:apply-templates/>
    <xsl:text disable-output-escaping="yes">&lt;/span&gt;</xsl:text>
  </xsl:template>

  <!-- 10) Scribal deletions: keep the genetic record, struck through.
       The trailing space replaces the whitespace text node that
       strip-space removes before a following inline element. -->
  <xsl:template match="tei:del">
    <xsl:text disable-output-escaping="yes">&lt;span class="del"&gt;</xsl:text>
    <xsl:apply-templates/>
    <xsl:text disable-output-escaping="yes">&lt;/span&gt; </xsl:text>
  </xsl:template>

  <!-- 11) Additions. Contemporary decipherments written above cipher
       passages get their own marker; other additions by another hand or in
       the margin are marked so they are not mistaken for the main text.
       The explicit priority keeps the decipher rule from being an ambiguous
       match against the rule below. -->
  <xsl:template match="tei:add[@type='decipher']" priority="1">
    <xsl:text disable-output-escaping="yes">&lt;span class="decipher" title="contemporary decipherment"&gt;</xsl:text>
    <xsl:apply-templates/>
    <xsl:text disable-output-escaping="yes">&lt;/span&gt; </xsl:text>
  </xsl:template>
  <xsl:template match="tei:add[@hand or @place]">
    <xsl:value-of disable-output-escaping="yes"
      select="concat('&lt;span class=&quot;add&quot; title=&quot;',
                     cav:attr(string-join((
                       'addition',
                       if (@place) then string(@place) else (),
                       if (@hand) then concat('hand ', substring-after(@hand, '#')) else ()
                     ), ', ')),
                     '&quot;&gt;')"/>
    <xsl:apply-templates/>
    <xsl:text disable-output-escaping="yes">&lt;/span&gt; </xsl:text>
  </xsl:template>
  <xsl:template match="tei:add">
    <xsl:apply-templates/>
  </xsl:template>

  <!-- 11b) Enciphered passages. Without a template these fell through to
       the catch-all and dumped a bare digit run straight into the reading
       text, with no space before the words that follow it. -->
  <xsl:template match="tei:seg[@type='cipher']">
    <xsl:value-of disable-output-escaping="yes"
      select="concat('&lt;span class=&quot;cipher&quot; title=&quot;',
                     cav:attr(string-join((
                       'enciphered passage',
                       if (@subtype) then concat(@subtype, ' cipher') else (),
                       if (@hand) then concat('hand ', substring-after(@hand, '#')) else ()
                     ), ', ')),
                     '&quot;&gt;')"/>
    <xsl:apply-templates/>
    <xsl:text disable-output-escaping="yes">&lt;/span&gt; </xsl:text>
  </xsl:template>

  <!-- 11c) Text supplied by the editor — decipherments and restorations.
       These are the editor's reconstruction, not the manuscript's words, so
       they are bracketed and marked. Without this they were indistinguishable
       from the transcription. -->
  <xsl:template match="tei:supplied">
    <xsl:value-of disable-output-escaping="yes"
      select="concat('&lt;span class=&quot;supplied&quot; title=&quot;',
                     cav:attr(string-join((
                       concat('supplied by the editor',
                              if (@reason) then concat(' (', @reason, ')') else ''),
                       if (@cert) then concat('certainty ', @cert) else ()
                     ), ', ')),
                     '&quot;&gt;[')"/>
    <xsl:apply-templates/>
    <xsl:text disable-output-escaping="yes">]&lt;/span&gt; </xsl:text>
  </xsl:template>

  <!-- 12) Foreign-language passages keep their language tag. -->
  <xsl:template match="tei:foreign">
    <xsl:value-of disable-output-escaping="yes"
      select="concat('&lt;em', if (@xml:lang) then concat(' lang=&quot;', cav:attr(@xml:lang), '&quot;') else '', '&gt;')"/>
    <xsl:apply-templates/>
    <xsl:text disable-output-escaping="yes">&lt;/em&gt;</xsl:text>
  </xsl:template>

  <!-- 13) Notes carry their type, placement, and hand. -->
  <xsl:template match="tei:note">
    <xsl:variable name="qualifiers" select="string-join((
        if (@type) then string(@type) else (),
        if (@place) then string(@place) else (),
        if (@hand) then concat('hand ', substring-after(@hand, '#')) else ()
      ), ', ')"/>
    <xsl:text>[NOTE</xsl:text>
    <xsl:if test="$qualifiers ne ''">
      <xsl:text> (</xsl:text>
      <xsl:value-of select="$qualifiers"/>
      <xsl:text>)</xsl:text>
    </xsl:if>
    <xsl:text>: </xsl:text>
    <xsl:apply-templates/>
    <xsl:text>]</xsl:text>
  </xsl:template>

  <!-- 14) Gaps and damage: report the extent when it is quantified, then
       the description of what is lost. -->
  <xsl:template match="tei:gap">
    <xsl:text>[missing</xsl:text>
    <xsl:choose>
      <xsl:when test="@quantity">
        <xsl:text> </xsl:text>
        <xsl:value-of select="@quantity"/>
        <xsl:if test="@unit">
          <xsl:text> </xsl:text>
          <xsl:value-of select="if (number(@quantity) = 1)
                                then replace(string(@unit), 's$', '')
                                else if (ends-with(string(@unit), 's')) then string(@unit)
                                else concat(string(@unit), 's')"/>
        </xsl:if>
      </xsl:when>
      <xsl:when test="@extent">
        <xsl:text> </xsl:text>
        <xsl:value-of select="normalize-space(@extent)"/>
      </xsl:when>
    </xsl:choose>
    <xsl:if test="tei:desc">
      <xsl:text>: </xsl:text>
      <xsl:value-of select="replace(normalize-space(tei:desc), '^[Nn]ote:\s*', '')"/>
    </xsl:if>
    <xsl:text>] </xsl:text>
  </xsl:template>

  <xsl:template match="tei:damage">
    <xsl:apply-templates/>
  </xsl:template>

  <!-- 15) Tables (e.g. cipher keys) become Markdown tables. The header
       separator is only emitted when there is more than one row. -->
  <xsl:template match="tei:table">
    <xsl:text>&#10;&#10;</xsl:text>
    <xsl:apply-templates/>
    <xsl:text>&#10;</xsl:text>
  </xsl:template>

  <xsl:template match="tei:row">
    <xsl:text>| </xsl:text>
    <xsl:for-each select="tei:cell">
      <xsl:apply-templates mode="cell"/>
      <xsl:text> | </xsl:text>
    </xsl:for-each>
    <xsl:text>&#10;</xsl:text>
    <xsl:if test="position() = 1 and count(../tei:row) &gt; 1">
      <xsl:text>|</xsl:text>
      <xsl:for-each select="tei:cell">
        <xsl:text>---|</xsl:text>
      </xsl:for-each>
      <xsl:text>&#10;</xsl:text>
    </xsl:if>
  </xsl:template>

  <!-- Cell content must stay on one line and must not contain a raw pipe. -->
  <xsl:template match="tei:lb | tei:pb" mode="cell">
    <xsl:text> </xsl:text>
  </xsl:template>
  <xsl:template match="text()" mode="cell">
    <xsl:value-of select="replace(., '\|', '\\|')"/>
  </xsl:template>
  <xsl:template match="*" mode="cell">
    <xsl:apply-templates mode="cell"/>
  </xsl:template>

  <xsl:template match="tei:label">
    <xsl:text>**</xsl:text>
    <xsl:apply-templates/>
    <xsl:text>**&#10;</xsl:text>
  </xsl:template>

  <!-- 16) Default TEI handling -->
  <xsl:template match="tei:*">
    <xsl:apply-templates/>
  </xsl:template>

  <!-- 17) All body text passes through MDX escaping. -->
  <xsl:template match="text()">
    <xsl:value-of select="cav:mdx(.)"/>
  </xsl:template>

</xsl:stylesheet>
