<?xml version="1.0" encoding="UTF-8"?>
<!-- XSLT for converting TEI letters to Docusaurus Markdown -->
<xsl:stylesheet
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:tei="http://www.tei-c.org/ns/1.0"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    exclude-result-prefixes="tei xs"
    version="2.0">

  <!-- Produce text output (not HTML), but we will embed raw HTML tags
       by escaping them and using disable-output-escaping. -->
  <xsl:output method="text" encoding="UTF-8"/>
  <xsl:strip-space elements="tei:*"/>

  <!-- 1)  Entry point: collect entire text, then strip spaces before punctuation. -->
  <xsl:template match="/">
    <xsl:variable name="rawOutput">
      <xsl:apply-templates select="tei:TEI"/>
    </xsl:variable>
    <xsl:value-of select="replace($rawOutput, '[ \t\r\n]+([,;:\.])', '$1')"/>
  </xsl:template>

  <!-- 2) Process root <TEI> to output front matter, then apply templates to the text. -->
  <xsl:template match="tei:TEI">
    <xsl:variable name="locusFrom" select="tei:teiHeader/tei:fileDesc/tei:sourceDesc/tei:msDesc/tei:msContents/tei:msItem/tei:locus/@from"/>
    <xsl:variable name="locusTo"   select="tei:teiHeader/tei:fileDesc/tei:sourceDesc/tei:msDesc/tei:msContents/tei:msItem/tei:locus/@to"/>

    <xsl:variable name="archiveRef" as="xs:string" 
      select="normalize-space(
        concat(
          tei:teiHeader/tei:fileDesc/tei:sourceDesc/tei:msDesc/tei:msIdentifier/tei:settlement, ' ',
          tei:teiHeader/tei:fileDesc/tei:sourceDesc/tei:msDesc/tei:msIdentifier/tei:repository, ', ',
          tei:teiHeader/tei:fileDesc/tei:sourceDesc/tei:msDesc/tei:msIdentifier/tei:collection, ', ',
          tei:teiHeader/tei:fileDesc/tei:sourceDesc/tei:msDesc/tei:msIdentifier/tei:idno,
          ', fols. ', $locusFrom, '-', $locusTo
        )
      )"/>

    <!-- YAML-like front matter for Markdown -->
    <xsl:text>---&#10;</xsl:text>

    <xsl:variable name="sentDate" select="tei:teiHeader/tei:profileDesc/tei:correspDesc/tei:correspAction[@type='sent']/tei:date"/>
    <xsl:variable name="dateValue" select="if ($sentDate/@when) then $sentDate/@when else if ($sentDate/@notBefore) then $sentDate/@notBefore else ''"/>

    <xsl:text>title: "</xsl:text>
    <xsl:value-of select="$dateValue"/>
    <xsl:text>"&#10;</xsl:text>

    <xsl:text>expeditor: "</xsl:text>
    <xsl:value-of select="tei:teiHeader/tei:profileDesc/tei:correspDesc/tei:correspAction[@type='sent']/tei:persName"/>
    <xsl:text>"&#10;</xsl:text>

    <xsl:text>addressee: "</xsl:text>
    <xsl:value-of select="tei:teiHeader/tei:profileDesc/tei:correspDesc/tei:correspAction[@type='received']/tei:persName"/>
    <xsl:text>"&#10;</xsl:text>

    <xsl:text>date: "</xsl:text>
    <xsl:value-of select="$dateValue"/>
    <xsl:text>"&#10;</xsl:text>

    <xsl:text>placeOfOrigin: "</xsl:text>
    <xsl:value-of select="tei:teiHeader/tei:profileDesc/tei:correspDesc/tei:correspAction[@type='sent']/tei:placeName"/>
    <xsl:text>"&#10;</xsl:text>

    <xsl:text>archiveRef: "</xsl:text>
    <xsl:value-of select="$archiveRef"/>
    <xsl:text>"&#10;</xsl:text>

    <xsl:text>---&#10;</xsl:text>
    <xsl:text>&#10;</xsl:text>

    <!-- Visible metadata block -->
    <xsl:variable name="sender"       select="tei:teiHeader/tei:profileDesc/tei:correspDesc/tei:correspAction[@type='sent']/tei:persName"/>
    <xsl:variable name="senderPlace"  select="tei:teiHeader/tei:profileDesc/tei:correspDesc/tei:correspAction[@type='sent']/tei:placeName"/>
    <xsl:variable name="sendDate"     select="tei:teiHeader/tei:profileDesc/tei:correspDesc/tei:correspAction[@type='sent']/tei:date"/>
    <xsl:variable name="receiver"     select="tei:teiHeader/tei:profileDesc/tei:correspDesc/tei:correspAction[@type='received']/tei:persName"/>
    <xsl:variable name="receiverPlace" select="tei:teiHeader/tei:profileDesc/tei:correspDesc/tei:correspAction[@type='received']/tei:placeName"/>
    <xsl:variable name="summary"      select="tei:teiHeader/tei:fileDesc/tei:sourceDesc/tei:msDesc/tei:msContents/tei:msItem/tei:note[@type='summary']"/>

    <xsl:text disable-output-escaping="yes">&lt;div class="letter-metadata"&gt;&#10;</xsl:text>
    <xsl:text>&#10;</xsl:text>
    <xsl:text>| | |&#10;</xsl:text>
    <xsl:text>|---|---|&#10;</xsl:text>

    <xsl:text>| **From** | </xsl:text>
    <xsl:value-of select="normalize-space($sender)"/>
    <xsl:if test="normalize-space($senderPlace) != ''">
      <xsl:text>, </xsl:text>
      <xsl:value-of select="normalize-space($senderPlace)"/>
    </xsl:if>
    <xsl:text> |&#10;</xsl:text>

    <xsl:text>| **To** | </xsl:text>
    <xsl:value-of select="normalize-space($receiver)"/>
    <xsl:if test="normalize-space($receiverPlace) != ''">
      <xsl:text>, </xsl:text>
      <xsl:value-of select="normalize-space($receiverPlace)"/>
    </xsl:if>
    <xsl:text> |&#10;</xsl:text>

    <xsl:text>| **Date** | </xsl:text>
    <xsl:value-of select="normalize-space($sendDate)"/>
    <xsl:text> |&#10;</xsl:text>

    <xsl:text>| **Archive** | </xsl:text>
    <xsl:value-of select="$archiveRef"/>
    <xsl:text> |&#10;</xsl:text>

    <xsl:if test="normalize-space($summary) != ''">
      <xsl:text>| **Summary** | </xsl:text>
      <xsl:value-of select="normalize-space($summary)"/>
      <xsl:text> |&#10;</xsl:text>
    </xsl:if>

    <!-- Suggested citation -->
    <xsl:variable name="editor" select="tei:teiHeader/tei:fileDesc/tei:titleStmt/tei:editor"/>
    <xsl:variable name="letterTitle" select="tei:teiHeader/tei:fileDesc/tei:titleStmt/tei:title"/>
    <xsl:text>| **Cite as** | </xsl:text>
    <xsl:value-of select="normalize-space($editor)"/>
    <xsl:text> (ed.), "</xsl:text>
    <xsl:value-of select="normalize-space($letterTitle)"/>
    <xsl:text>," in *Filippo Cavriana: The Secret Correspondence*, accessed 31 March 2026, https://pantagrueliste.github.io/CavrianaCorr_FrontEnd/ |&#10;</xsl:text>

    <xsl:text>&#10;</xsl:text>
    <xsl:text disable-output-escaping="yes">&lt;/div&gt;&#10;</xsl:text>
    <xsl:text>&#10;</xsl:text>

    <!-- Beta disclaimer -->
    <xsl:text disable-output-escaping="yes">&lt;div class="beta-notice"&gt;&#10;</xsl:text>
    <xsl:text>&#10;</xsl:text>
    <xsl:text>:::caution Beta version&#10;</xsl:text>
    <xsl:text>This digital edition is currently in **beta** (stage one of publication is in progress). Transcription quality cannot yet be fully guaranteed. Please exercise caution when citing this document, and verify readings against the original manuscript when possible.&#10;</xsl:text>
    <xsl:text>:::&#10;</xsl:text>
    <xsl:text>&#10;</xsl:text>
    <xsl:text disable-output-escaping="yes">&lt;/div&gt;&#10;</xsl:text>
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
  <xsl:template match="tei:lb[@break='no']">
    <xsl:text disable-output-escaping="yes">-&lt;br/&gt;&#10;</xsl:text>
  </xsl:template>
  <xsl:template match="tei:lb">
    <xsl:text disable-output-escaping="yes">&lt;br/&gt;&#10;</xsl:text>
  </xsl:template>

  <!-- 6) Paragraph-like elements -->
  <xsl:template match="tei:p | tei:opener | tei:closer | tei:postscript">
    <xsl:apply-templates/>
    <xsl:text>&#10;&#10;</xsl:text>
  </xsl:template>

  <!-- 7) persName/placeName -->
  <xsl:template match="tei:persName | tei:placeName">
    <xsl:value-of select="normalize-space(.)"/>
  </xsl:template>

  <!-- 7) <choice>: only show <expan>, ignore <abbr> -->
  <xsl:template match="tei:choice">
    <xsl:value-of select="tei:expan"/>
    <xsl:text> </xsl:text>
  </xsl:template>
  <xsl:template match="tei:choice/tei:abbr"/>

  <!-- 8) UNCLEAR words -->
  <xsl:template match="tei:unclear">
    <xsl:text disable-output-escaping="yes">&lt;span class="unclear"&gt;</xsl:text>
    <xsl:apply-templates/>
    <xsl:text disable-output-escaping="yes">&lt;/span&gt;</xsl:text>
  </xsl:template>

  <!-- 8) Skip <del> -->
  <xsl:template match="tei:del"/>

  <!-- 9) <add> inline -->
  <xsl:template match="tei:add">
    <xsl:apply-templates/>
  </xsl:template>

  <!-- 8) Note handling -->
  <xsl:template match="tei:note">
    <xsl:text>[NOTE: </xsl:text>
    <xsl:apply-templates/>
    <xsl:text>]</xsl:text>
  </xsl:template>

  <!-- 9) Gaps and damage -->
  <xsl:template match="tei:gap">
    <xsl:text>[missing </xsl:text>
    <xsl:value-of select="@quantity"/>
    <xsl:text> </xsl:text>
    <xsl:value-of select="@unit"/>
    <xsl:text>]</xsl:text>
  </xsl:template>

  <xsl:template match="tei:damage">
    <xsl:apply-templates/>
  </xsl:template>

  <!-- 9) Default TEI handling -->
  <xsl:template match="tei:*">
    <xsl:apply-templates/>
  </xsl:template>

</xsl:stylesheet>
