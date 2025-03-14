<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet 
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform" 
    xmlns:tei="http://www.tei-c.org/ns/1.0"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    exclude-result-prefixes="tei xs"
    version="2.0">

  <xsl:output method="text" encoding="UTF-8"/>
  <xsl:strip-space elements="tei:*"/>

  <!-- 
    ============ ENTRY POINT ============
    Collect main output into $rawOutput, then
    remove unwanted spaces before punctuation.
  -->
  <xsl:template match="/">
    <xsl:variable name="rawOutput">
      <xsl:apply-templates select="tei:TEI"/>
    </xsl:variable>
    <!-- For removing only spaces/tabs before punctuation, use e.g. [ \t]+ -->
    <xsl:value-of select="replace($rawOutput, '[ \t\r\n]+([,;:\.])', '$1')"/>
  </xsl:template>

  <!-- 
    ============ MAIN TEI ============ 
    Output metadata as front matter, then text.
  -->
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

    <xsl:text>---&#10;</xsl:text>

    <!-- If you prefer a fallback title from <title> in <titleStmt>, you can adapt here -->
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

    <!-- Now apply to the text body -->
    <xsl:apply-templates select="tei:text"/>
  </xsl:template>

  <!-- 
    ============ TEXT & STRUCTURE ============
    Usually just pass through <text>, capturing <body> etc. 
  -->
  <xsl:template match="tei:text">
    <xsl:apply-templates/>
  </xsl:template>

  <!-- Paragraph-like blocks: put blank lines after them -->
  <xsl:template match="tei:p | tei:opener | tei:closer | tei:postscript">
    <xsl:apply-templates/>
    <xsl:text>&#10;&#10;</xsl:text>
  </xsl:template>

  <!-- Page break: insert bracketed note and blank lines -->
  <xsl:template match="tei:pb">
    <xsl:text>&#10;**[fol. </xsl:text>
    <xsl:value-of select="@n"/>
    <xsl:text>]**&#10;&#10;</xsl:text>
  </xsl:template>

  <!-- Line break logic: if break='no' add a dash at the end of that line -->
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

  <!-- 
    ============ LOW-LEVEL TEXT HANDLING ============
    <choice> typically has <abbr> and <expan>. Below you see 
    we output only the expansion. Adapt if you wish to show both. 
  -->
  <xsl:template match="tei:choice">
    <xsl:value-of select="tei:expan"/>
    <xsl:text> </xsl:text>
  </xsl:template>
  <!-- Abbreviation: ignoring it, so it doesn't appear twice -->
  <xsl:template match="tei:choice/tei:abbr"/>

  <!-- Names: normalised text -->
  <xsl:template match="tei:persName | tei:placeName">
    <xsl:value-of select="normalize-space(.)"/>
  </xsl:template>

  <!-- If <unclear>, just output text. Could also add brackets if you wish: [unclear text] -->
  <xsl:template match="tei:unclear">
    <xsl:value-of select="."/>
  </xsl:template>

  <!-- <del> is usually omitted in a diplomatic reading text. Adjust if you want to show it. -->
  <xsl:template match="tei:del"/>

  <!-- <add> is printed inline. Adjust if you want special formatting. -->
  <xsl:template match="tei:add">
    <xsl:value-of select="."/>
  </xsl:template>

  <!-- 
    ============ COMMON TEI EXTENSIONS ============
    Below are optional templates for editorial notes, damage, gaps, etc. 
  -->

  <!-- 1) TEI <note> handling -->
  <xsl:template match="tei:note">
    <!-- Only show editorial notes, or show them all? 
         Here, we show all notes in square brackets. -->
    <xsl:text>[NOTE: </xsl:text>
    <xsl:apply-templates/>
    <xsl:text>]</xsl:text>
  </xsl:template>

  <!-- 2) TEI <gap> handling -->
  <xsl:template match="tei:gap">
    <!-- Example: show a placeholder with missing info 
         (e.g. reason="hole", quantity="3", unit="words") -->
    <xsl:text>[missing </xsl:text>
    <xsl:value-of select="@quantity"/>
    <xsl:text> </xsl:text>
    <xsl:value-of select="@unit"/>
    <xsl:text>]</xsl:text>
  </xsl:template>

  <!-- 3) TEI <damage> often contains <gap>. 
       Simply pass contents so <gap> gets handled. -->
  <xsl:template match="tei:damage">
    <xsl:apply-templates/>
  </xsl:template>

  <!-- 4) TEI <seg> (or other unhandled elements) 
       If you want them just to flow inline, apply templates. -->
  <xsl:template match="tei:seg">
    <xsl:apply-templates/>
  </xsl:template>

  <!-- Finally, a catch-all for anything we did not match explicitly:
       just apply templates so text children still appear. -->
  <xsl:template match="tei:*">
    <xsl:apply-templates/>
  </xsl:template>

</xsl:stylesheet>
