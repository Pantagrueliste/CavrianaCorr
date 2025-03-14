<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet 
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:tei="http://www.tei-c.org/ns/1.0"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    exclude-result-prefixes="tei xs"
    version="2.0">

  <xsl:output method="text" encoding="UTF-8"/>
  <xsl:strip-space elements="tei:*"/>

  <!-- Entry point: collect everything, then remove spaces before punctuation. -->
  <xsl:template match="/">
    <xsl:variable name="rawOutput">
      <xsl:apply-templates select="tei:TEI"/>
    </xsl:variable>
    <xsl:value-of select="replace($rawOutput, '[ \t\r\n]+([,;:\.])', '$1')"/>
  </xsl:template>

  <!-- Process the TEI as a whole: output metadata, then text. -->
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

    <!-- Front matter in Markdown-like format -->
    <xsl:text>---&#10;</xsl:text>
    <xsl:text>title: "</xsl:text>
    <xsl:value-of select="concat(
      tei:teiHeader/tei:profileDesc/tei:correspDesc/tei:correspAction[@type='received']/tei:persName,
      ' (',
      tei:teiHeader/tei:profileDesc/tei:correspDesc/tei:correspAction[@type='sent']/tei:date/@when,
      ')'
    )"/>
    <xsl:text>"&#10;</xsl:text>

    <xsl:text>expeditor: "</xsl:text>
    <xsl:value-of select="tei:teiHeader/tei:profileDesc/tei:correspDesc/tei:correspAction[@type='sent']/tei:persName"/>
    <xsl:text>"&#10;</xsl:text>

    <xsl:text>addressee: "</xsl:text>
    <xsl:value-of select="tei:teiHeader/tei:profileDesc/tei:correspDesc/tei:correspAction[@type='received']/tei:persName"/>
    <xsl:text>"&#10;</xsl:text>

    <xsl:text>date: "</xsl:text>
    <xsl:value-of select="tei:teiHeader/tei:profileDesc/tei:correspDesc/tei:correspAction[@type='sent']/tei:date/@when"/>
    <xsl:text>"&#10;</xsl:text>

    <xsl:text>placeOfOrigin: "</xsl:text>
    <xsl:value-of select="tei:teiHeader/tei:profileDesc/tei:correspDesc/tei:correspAction[@type='sent']/tei:placeName"/>
    <xsl:text>"&#10;</xsl:text>

    <xsl:text>archiveRef: "</xsl:text>
    <xsl:value-of select="$archiveRef"/>
    <xsl:text>"&#10;</xsl:text>

    <xsl:text>---&#10;</xsl:text>
    <xsl:text>&#10;</xsl:text>

    <!-- Body text. -->
    <xsl:apply-templates select="tei:text"/>
  </xsl:template>

  <!-- Text wrapper: apply templates to children. -->
  <xsl:template match="tei:text">
    <xsl:apply-templates/>
  </xsl:template>

  <!-- Page breaks. -->
  <xsl:template match="tei:pb">
    <xsl:text>&#10;**[fol. </xsl:text>
    <xsl:value-of select="@n"/>
    <xsl:text>]**&#10;&#10;</xsl:text>
  </xsl:template>

  <!-- Line breaks. -->
  <xsl:template match="tei:lb">
    <xsl:choose>
      <xsl:when test="@break = 'no'">
        <xsl:text>-  &#10;</xsl:text>
      </xsl:when>
      <xsl:otherwise>
        <xsl:text>  &#10;</xsl:text>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>

  <!-- Paragraphs, openers, closers, etc.  -->
  <xsl:template match="tei:p | tei:opener | tei:closer | tei:postscript">
    <xsl:apply-templates/>
    <xsl:text>&#10;&#10;</xsl:text>
  </xsl:template>

  <!-- Names. -->
  <xsl:template match="tei:persName | tei:placeName">
    <xsl:value-of select="normalize-space(.)"/>
  </xsl:template>

  <!-- Choice expansions. -->
  <xsl:template match="tei:choice">
    <xsl:value-of select="tei:expan"/>
    <xsl:text> </xsl:text>
  </xsl:template>
  <xsl:template match="tei:choice/tei:abbr"/>

  <!-- Unclear words => <span class="unclear"> -->
  <xsl:template match="tei:unclear">
    <xsl:text><span class="unclear"> </xsl:text>
    <xsl:value-of select="."/>
    <xsl:text></span></xsl:text>
  </xsl:template>

  <!-- Deletions skipped. -->
  <xsl:template match="tei:del"/>

  <!-- Additions output inline. -->
  <xsl:template match="tei:add">
    <xsl:value-of select="."/>
  </xsl:template>

  <!-- Notes, if desired. -->
  <xsl:template match="tei:note">
    <xsl:text>[NOTE: </xsl:text>
    <xsl:apply-templates/>
    <xsl:text>]</xsl:text>
  </xsl:template>

  <!-- Gaps and damage. -->
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

  <!-- Seg and anything not explicitly matched. -->
  <xsl:template match="tei:seg">
    <xsl:apply-templates/>
  </xsl:template>

  <xsl:template match="tei:*">
    <xsl:apply-templates/>
  </xsl:template>

</xsl:stylesheet>
